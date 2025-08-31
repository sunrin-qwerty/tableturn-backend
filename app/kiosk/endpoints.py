from typing import Annotated, Any

import aredis_om.model.model
import tortoise.exceptions
from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, Depends, Body
from fastapi_restful.cbv import cbv

from app.auth.services import AuthService
from app.common.authorization.kiosk import get_current_kiosk_entity
from app.common.exceptions import APIError
from app.common.exceptions.auth_exception import NotFound, PermissionDenied
from app.containers import AppContainers
from app.common.server import APIResponse
from app.google.services import GoogleService
from app.kiosk.services import KioskService

from app.kiosk.dto import RequestSessionAuthenticateDTO
from app.common.authorization import get_current_user_entity
from app.members.entities import MemberEntity
from app.kiosk.entities import KioskAccountEntity

from app.common.utils.generate import generate_key

router = APIRouter(
    prefix="/kiosk",
    tags=["Kiosk"],
    responses={404: {"description": "Not found"}},
)


@cbv(router)
class KioskEndpoint:

    @router.post(
        "/session/create",
        description="키오스크 계정 로그인 세션 생성",
    )
    @inject
    async def session_create(
        self,
        kiosk_service: KioskService = Depends(Provide[AppContainers.kiosk.service]),
        user_agent: str = Body(..., embed=True, title="User Agent"),
    ) -> APIResponse[dict]:
        session_id = await kiosk_service.create_session(user_agent)
        return APIResponse(
            message="Session Created",
            data={"session_id": session_id, "expired_in": 60 * 5},
        )  # 5분

    @router.get("/session/{session_id}", description="키오스크 세션 인증 여부 확인")
    @inject
    async def get_session(
        self,
        session_id: str,
        kiosk_service: KioskService = Depends(Provide[AppContainers.kiosk.service]),
        # _user: MemberEntity = Depends(get_current_user_entity),
    ) -> APIResponse[dict]:
        try:
            session = await kiosk_service.get_session(session_id)
        except aredis_om.model.model.NotFoundError:
            raise NotFound(message="Session Not Found")
        return APIResponse(
            message="Session Retrieved",
            data={
                "is_authenticated": session.is_authenticated,
                "name": session.name,
                "table_id": session.table_id,
                "login_key": session.login_key,
            },
        )

    @router.get("/test")
    @inject
    async def test(self, _user: KioskAccountEntity = Depends(get_current_kiosk_entity)):
        return {}

    @router.post(
        "/session/authenticate",
        description="관리자가 키오스크 세션을 로그인시키는 부분",
    )
    @inject
    async def session_authenticate(
        self,
        user: MemberEntity = Depends(get_current_user_entity),
        kiosk_service: KioskService = Depends(Provide[AppContainers.kiosk.service]),
        data: RequestSessionAuthenticateDTO = Body(
            ..., title="Request Session Authenticate"
        ),
    ) -> APIResponse[dict]:
        if not user.is_admin:
            raise PermissionDenied(message="Permission Denied")

        try:
            session = await kiosk_service.get_session(data.session_id)
        except aredis_om.model.model.NotFoundError:
            raise NotFound(message="Session Not Found")

        if await KioskAccountEntity.exists(table_id=session.table_id):
            raise APIError(message="Table ID already in use")

        login_key = generate_key(35)

        account = await KioskAccountEntity.create(
            name=data.name,
            table_id=data.table_id,
            token=login_key,
        )

        await kiosk_service.authenticate_session(data.session_id, account)
        return APIResponse(
            message="Session Authenticated",
            data={
                "name": account.name,
                "table_id": account.table_id,
                "token": account.token,
            },
        )
