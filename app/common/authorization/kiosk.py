from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, HTTPDigest
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param

from jwt import PyJWTError, decode as jwt_decode
from starlette.status import HTTP_403_FORBIDDEN

from app.common.utils.env_validator import settings
from app.common.types import KIOSK_ID

from app.members.entities import MemberEntity
from app.kiosk.entities import KioskAccountEntity

from fastapi import Request
from fastapi.security.api_key import APIKeyHeader

__all__ = ["get_current_kiosk_id", "get_current_kiosk_entity"]


api_key_header = APIKeyHeader(name="X-Kiosk-Key", auto_error=False)


async def get_kiosk_key(api_key: str = Security(api_key_header)) -> str:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="X-Kiosk-Key header missing"
        )
    return api_key


async def get_current_kiosk_id(
    credential: str = Security(get_kiosk_key),
) -> KIOSK_ID:
    try:

        payload = await KioskAccountEntity.get_or_none(token=credential)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

        return payload.id
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )


async def get_current_kiosk_entity(
    credential: str = Security(get_kiosk_key),
) -> KioskAccountEntity:
    try:

        payload = await KioskAccountEntity.get_or_none(token=credential)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

        return payload

    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )
