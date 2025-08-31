from typing import Annotated, Any

import aredis_om.model.model
from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, Depends, Body
from fastapi_restful.cbv import cbv

from app.auth.services import AuthService
from app.common.authorization.kiosk import (
    get_current_kiosk_entity,
    get_current_kiosk_id,
)
from app.common.exceptions import APIError
from app.common.exceptions.auth_exception import NotFound, PermissionDenied
from app.containers import AppContainers
from app.common.server import APIResponse
from app.game.services import GameService
from app.google.services import GoogleService
from app.kiosk.services import KioskService

from app.kiosk.dto import RequestSessionAuthenticateDTO
from app.common.authorization import get_current_user_entity
from app.members.entities import MemberEntity
from app.kiosk.entities import KioskAccountEntity

from app.common.utils.generate import generate_key

router = APIRouter(
    prefix="/game",
    tags=["Game"],
    responses={404: {"description": "Not found"}},
)


@cbv(router)
class GameEndpoint:

    @router.get(
        "/list",
        description="게임 목록 조회",
    )
    @inject
    async def game_list(
        self, _kiosk_id: str = Depends(get_current_kiosk_id)
    ) -> APIResponse[dict]: ...

    @router.get(
        "/{game_id}",
        description="게임 상세 조회",
    )
    @inject
    async def game_detail(
        self, game_id: str, _kiosk_id: str = Depends(get_current_kiosk_id)
    ) -> APIResponse[dict]: ...

    @router.post("/admin/create", description="게임 생성")
    @inject
    async def game_create(
        self,
        name: str = Body(..., embed=True, title="게임 이름"),
        description: str | None = Body(None, embed=True, title="게임 설명"),
        theme: list[str] | None = Body(None, embed=True, title="게임 테마"),
        min_player_count: int | None = Body(1, embed=True, title="최소 플레이어 수"),
        max_player_count: int | None = Body(2, embed=True, title="최대 플레이어 수"),
        user: MemberEntity = Depends(get_current_user_entity),
        game_service: GameService = Depends(Provide[AppContainers.game.service]),
    ) -> APIResponse[dict]:
        if not user.is_admin:
            raise PermissionDenied("관리자 권한이 필요합니다.")
        game = await game_service.create(
            name=name,
            description=description,
            theme=theme,
            min_player_count=min_player_count,
            max_player_count=max_player_count,
        )
