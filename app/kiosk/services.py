from jwt import encode as jwt_encode, decode as jwt_decode, PyJWTError
from passlib.context import CryptContext
import aiogoogle

from app.common.types import SESSION_ID
from app.common.utils.env_validator import settings
from app.common.utils.logger import use_logger
from app.google.services import GoogleService
from app.common.exceptions import AuthenticateFailed
from app.kiosk.entities import KioskAccountEntity
from app.kiosk.repository import KioskRepository
from app.kiosk.session import KioskLoginSession

logger = use_logger("kiosk_service")


class KioskService:
    def __init__(self, kiosk_repository: KioskRepository) -> None:
        self.kiosk_repository = kiosk_repository

    async def create_session(self, user_agent: str) -> SESSION_ID:
        session_id = await self.kiosk_repository.create_session(user_agent)
        return session_id

    async def get_session(self, session_id: str) -> KioskLoginSession:
        session = await self.kiosk_repository.get_session(session_id)
        return session

    async def authenticate_session(
        self, session_id: SESSION_ID, account: KioskAccountEntity
    ) -> KioskLoginSession:
        session = await self.kiosk_repository.authenticate_session(session_id, account)
        return session

    async def revoke_session(self, session_id: SESSION_ID) -> None:
        await self.kiosk_repository.revoke_session(session_id)
