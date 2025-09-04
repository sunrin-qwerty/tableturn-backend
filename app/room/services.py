from jwt import encode as jwt_encode, decode as jwt_decode, PyJWTError
from passlib.context import CryptContext
import aiogoogle

from app.common.types import SESSION_ID, ROOM_ID
from app.common.utils.env_validator import settings
from app.common.utils.logger import use_logger
from app.google.services import GoogleService
from app.common.exceptions import AuthenticateFailed
from app.kiosk.entities import KioskAccountEntity
from app.kiosk.repository import KioskRepository
from app.kiosk.session import KioskLoginSession
from app.room.repository import RoomRepository
from app.room.session import SessionRoom

logger = use_logger("room_service")


class RoomService:
    def __init__(self, room_repository: RoomRepository) -> None:
        self.room_repository = room_repository

    async def create(self, kiosk_id: str) -> ROOM_ID:
        room_id = await self.room_repository.create(kiosk_id)
        return room_id

    async def close(self, room_id: str) -> None:
        await self.room_repository.close(room_id)

    async def get(self, room_id: str) -> SessionRoom:
        room = await self.room_repository.get(room_id)
        if not room:
            raise ValueError("Invalid room ID")
        return room

