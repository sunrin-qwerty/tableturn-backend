from app.kiosk.entities import KioskAccountEntity
from app.kiosk.session import KioskLoginSession

from app.common.types import SESSION_ID


class KioskRepository:

    @classmethod
    async def create_session(cls, user_agent: str) -> SESSION_ID:
        session = KioskLoginSession(is_authenticated=False, user_agent=user_agent)
        await session.save()
        await session.expire(num_seconds=60 * 5)
        return session.pk

    @classmethod
    async def is_authenticated(cls, session_id: SESSION_ID) -> bool:
        session = await KioskLoginSession.get(session_id)
        if not session:
            return False
        return session.is_authenticated

    @classmethod
    async def get_session(cls, session_id: SESSION_ID) -> KioskLoginSession:
        session = await KioskLoginSession.get(session_id)
        if not session:
            raise ValueError("Invalid session ID")
        return session

    @classmethod
    async def authenticate_session(
        cls, session_id: SESSION_ID, account: KioskAccountEntity
    ) -> KioskLoginSession:
        session = await cls.get_session(session_id)
        session.is_authenticated = True
        session.name = account.name
        session.table_id = account.table_id
        session.login_key = account.login_key
        await session.save()
        return session

    @classmethod
    async def revoke_session(cls, session_id: SESSION_ID) -> None:
        session = await cls.get_session(session_id)
        await session.delete(session_id)
