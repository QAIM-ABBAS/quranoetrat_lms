from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import AuthenticationError, PermissionDeniedError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = decode_access_token(token)
    except ValueError as exc:
        raise AuthenticationError("Invalid or expired authentication token") from exc

    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationError("Invalid authentication token")

    user = await db.get(User, int(user_id))
    if not user or not user.is_active:
        raise AuthenticationError("User is not active")

    return user


def require_role(*roles: str):
    async def dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role.value not in roles:
            raise PermissionDeniedError(
                f"Role '{current_user.role.value}' is not allowed to access this resource"
            )
        return current_user

    return dependency
