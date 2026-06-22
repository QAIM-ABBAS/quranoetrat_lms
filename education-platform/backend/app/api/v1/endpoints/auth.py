from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationError
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, TokenResponse, UserOut
from app.crud import user as user_crud

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    user = await user_crud.get_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise AuthenticationError("Incorrect email or password")

    if not user.is_active:
        raise AuthenticationError("User account is inactive")

    access_token = create_access_token(
        subject=user.id,
        extra_claims={"role": user.role.value},
    )
    return LoginResponse(
        access_token=access_token,
        user=UserOut(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role.value,
        ),
    )
