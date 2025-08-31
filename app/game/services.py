from jwt import encode as jwt_encode, decode as jwt_decode, PyJWTError
from passlib.context import CryptContext
import aiogoogle

from app.common.types import SESSION_ID
from app.common.utils.env_validator import settings
from app.common.utils.logger import use_logger
from app.common.utils.types import MISSING
from app.game.entities import GameEntity
from app.game.repository import GameRepository
from app.google.services import GoogleService
from app.common.exceptions import AuthenticateFailed
from app.kiosk.entities import KioskAccountEntity
from app.kiosk.repository import KioskRepository
from app.kiosk.session import KioskLoginSession

logger = use_logger("game_service")


class GameService:
    def __init__(self, game_repository: GameRepository) -> None:
        self.game_repository = game_repository

    async def create(
        self,
        name: str,
        description: str | None = None,
        theme: list | None = MISSING,
        min_player_count: int | None = 1,
        max_player_count: int | None = 2,
    ) -> GameEntity:
        return await self.game_repository.create(
            name=name,
            description=description,
            theme=theme,
            min_player_count=min_player_count,
            max_player_count=max_player_count,
        )

    async def get(self, game_id: str, /) -> GameEntity:
        return await self.game_repository.get_by_id(game_id)

    async def exist(self, *args, **kwargs) -> bool:
        return await self.game_repository.exist(*args, **kwargs)

    async def list_all(self) -> list[GameEntity]:
        return await self.game_repository.list_all()

    async def modify(self, entity_id: str, **kwargs) -> GameEntity:
        return await self.game_repository.modify(entity_id, **kwargs)

    async def delete(self, entity_id: str) -> None:
        return await self.game_repository.delete(entity_id)
