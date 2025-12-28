from fastapi import APIRouter, Depends, Security

from app.db.database import get_db_session, AsyncSession
from app.models.user import User
from app.schemas.user import (
    UserSchema,
    UserSignInSchema,
    UserCreateSchema,
    UserUpdateSchema,
)
from app.schemas.jwt import TokenSchema
from app.services.user import UserService, get_user_service
from app.auth.universal_jwt import get_current_user

router = APIRouter(prefix="/user", tags=["users"])


@router.post("/signup", response_model=UserSchema)
async def create(
    data: UserCreateSchema,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_db_session),
):
    return await user_service.create(data, session)


@router.post("/login", response_model=TokenSchema)
async def login(
    data: UserSignInSchema,
    session: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service),
) -> TokenSchema:
    return await user_service.authenticate(data, session)


@router.get("/me", response_model=UserSchema)
async def me(current_user: User = Security(get_current_user)) -> User:
    return current_user


@router.patch("/me", response_model=UserSchema)
async def update(
    data: UserUpdateSchema,
    current_user: User = Security(get_current_user),
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    return await user_service.update(current_user.id, data, session)
