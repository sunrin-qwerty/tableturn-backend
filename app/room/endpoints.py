from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, Depends, Body
from fastapi_restful.cbv import cbv

from app.auth.services import AuthService
from app.common.authorization import get_current_user_entity
from app.common.authorization.kiosk import get_current_kiosk_entity
from app.common.exceptions.auth_exception import PermissionDenied
from app.containers import AppContainers
from app.common.server import APIResponse
from app.google.services import GoogleService
from app.kiosk.entities import KioskAccountEntity
from app.members.entities import MemberEntity
from app.room.services import RoomService

from app.common.utils.env_validator import settings

router = APIRouter(
    prefix="/room",
    tags=["Room"],
    responses={404: {"description": "Not found"}},
)


@cbv(router)
class GameRoomEndpoint:
    @router.get("/app/start")
    @inject
    async def kiosk_start_app(
        self,
        kiosk: KioskAccountEntity = Depends(get_current_kiosk_entity),
        service: RoomService = Depends(Provide[AppContainers.room.service]),
    ) -> APIResponse[dict]:
        room_id = await service.create(str(kiosk.id))
        return APIResponse(
            message="방을 생성했습니다.",
            data={
                "room_id": room_id,
                "join_url": f"{settings.FRONTEND_URL}/join/{room_id}",
            },
        )

    @router.delete("/{room_id}/close")
    @inject
    async def kiosk_close_room(
        self,
        room_id: str,
        user: MemberEntity = Depends(get_current_user_entity),
        service: RoomService = Depends(Provide[AppContainers.room.service]),
    ) -> APIResponse[dict]:
        if not user.is_admin:
            raise PermissionDenied(message="권한이 없습니다.")
        await service.close(room_id)
        return APIResponse(message="방을 종료했습니다.")

    @router.get("/{room_id}")
    @inject
    async def get_room_info(
        self,
        room_id: str,
        user: MemberEntity = Depends(get_current_user_entity),
        service: RoomService = Depends(Provide[AppContainers.room.service]),
    ) -> APIResponse[dict]:
        if not user.is_admin:
            raise PermissionDenied(message="권한이 없습니다.")
        room = await service.get(room_id)
        return APIResponse(
            message="방 정보를 불러왔습니다.",
            data={
                "room_id": room.pk,
                "kiosk_id": room.kiosk_id,
                "game": {
                    "gid": room.game.gid,
                    "name": room.game.name,
                    "max_player_count": room.game.max_player_count,
                    "current_players": room.game.current_players,
                },
                "members": [
                    {
                        "member_id": member.member_id,
                        "name": member.name,
                        "avatar": member.avatar,
                        "is_host": member.is_host,
                    }
                    for member in room.members
                ],
                "created_at": room.created_at,
                "updated_at": room.updated_at,
            },
        )
