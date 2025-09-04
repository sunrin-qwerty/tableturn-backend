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
from app.game.entities.game import GameEntityCreate_Pydantic, GameEntity_Pydantic
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
        self,
        service: GameService = Depends(Provide[AppContainers.game.service]),
    ) -> APIResponse[dict]:
        entities = await service.list_all()
        return APIResponse(
            message="Game entity list",
            data={
                "games": [
                    GameEntity_Pydantic(
                        id=entity.id,
                        name=entity.name,
                        description=entity.description,
                        theme=entity.theme,
                        min_player_count=entity.min_player_count,
                        max_player_count=entity.max_player_count,
                    )
                    for entity in entities
                ]
            },
        )

    @router.get("/{game_id}", description="게임 상세 조회")
    @inject
    async def game_detail(
        self,
        game_id: str,
        service: GameService = Depends(Provide[AppContainers.game.service]),
    ) -> APIResponse[dict]:
        entity = await service.get(game_id)
        return APIResponse(
            message="Game entity detail",
            data=GameEntity_Pydantic(
                id=entity.id,
                name=entity.name,
                description=entity.description,
                theme=entity.theme,
                min_player_count=entity.min_player_count,
                max_player_count=entity.max_player_count,
            ).model_dump(),
        )

    @router.post("/create", description="게임 생성")
    @inject
    async def game_create(
        self,
        data: GameEntityCreate_Pydantic = Body(...),
        user: MemberEntity = Depends(get_current_user_entity),
        service: GameService = Depends(Provide[AppContainers.game.service]),
    ) -> APIResponse[dict]:
        if not user.is_admin:
            raise PermissionDenied("관리자 권한이 필요합니다.")

        entity = await service.create(**data.dict())
        return APIResponse(message="Game entity created", data={"id": str(entity.id)})

    @router.delete("/{game_id}", description="게임 삭제")
    @inject
    async def game_delete(
        self,
        game_id: str,
        user: MemberEntity = Depends(get_current_user_entity),
        service: GameService = Depends(Provide[AppContainers.game.service]),
    ) -> APIResponse[dict]:
        if not user.is_admin:
            raise PermissionDenied("관리자 권한이 필요합니다.")

        await service.delete(game_id)
        return APIResponse(message="Game entity deleted", data={"id": game_id})

    @router.put("/{game_id}", description="게임 수정")
    @inject
    async def game_modify(
        self,
        game_id: str,
        data: GameEntityCreate_Pydantic = Body(...),
        user: MemberEntity = Depends(get_current_user_entity),
        service: GameService = Depends(Provide[AppContainers.game.service]),
    ) -> APIResponse[dict]:
        if not user.is_admin:
            raise PermissionDenied("관리자 권한이 필요합니다.")

        entity = await service.modify(game_id, **data.dict())
        return APIResponse(message="Game entity modified", data={"id": str(entity.id)})
