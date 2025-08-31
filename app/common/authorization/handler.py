from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jwt import PyJWTError, decode as jwt_decode
from app.common.utils.env_validator import settings
from app.common.types import USER_ID

from app.members.entities import MemberEntity

security = HTTPBearer(description="User Authorization Token")

__all__ = ["get_current_user_id", "get_current_user_entity"]


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> USER_ID:
    try:
        token = credentials.credentials

        payload = jwt_decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

        user_id: str = payload.get("uid")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

        return user_id

    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )


async def get_current_user_entity(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> MemberEntity:
    try:
        token = credentials.credentials

        payload = jwt_decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

        user_id: str = payload.get("uid")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

        user = await MemberEntity.get_or_none(id=user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )
        return user

    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )
