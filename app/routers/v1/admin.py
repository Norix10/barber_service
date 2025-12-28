from fastapi import APIRouter, Depends, Security

from app.core.config import settings
from app.db.database import AsyncSession, get_db_session
from app.services.admin import AdminService, get_admin_service
from app.services.user import UserService, get_user_service
from app.schemas.admin import (
    AdminBaseSchema,
    AdminSchema,
    AdminSignInSchema,
)
from app.schemas.user import (
    UserBaseSchema,
    UserSchema,
    UserSignInSchema,
    UserCreateSchema,
    UserUpdateSchema,
)
from app.schemas.jwt import TokenSchema, TokenDataSchema, FullTokenInfo, AccessTokenOnly
from app.models.admin import Admin
from app.auth.universal_jwt import get_current_admin


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login", response_model=TokenSchema)
async def login(
    data: AdminSignInSchema,
    session: AsyncSession = Depends(get_db_session),
    admin_service: AdminService = Depends(get_admin_service),
) -> TokenSchema:
    return await admin_service.authenticate(data, session)


@router.get("/me", response_model=AdminSchema)
async def me(current_admin: Admin = Security(get_current_admin)) -> Admin:
    return current_admin


@router.get("/all-users", response_model=list)
async def get_user_list(
    current_admin: Admin = Security(get_current_admin),
    session: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service),
) -> list:
    return await user_service.get_list(session)


@router.patch("/user/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int,
    data: UserUpdateSchema,
    current_admin: Admin = Security(get_current_admin),
    session: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service),
) -> UserSchema:
    return await user_service.update(user_id, data, session)


@router.delete("/user/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    current_admin: Admin = Security(get_current_admin),
    session: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service),
) -> None:
    user = await user_service.get_user_or_error(user_id, session)
    await user_service.delete(user, session)


# @router.post("/create-new-user", response_model=AdminResponse)
# async def create_new_user(
#     data: AdminCreate,
#     admin_service: AdminService = Depends(get_admin_service),
#     session: AsyncSession = Depends(get_db_session),
# ) -> Admin:
#     return await admin_service.create(data, session)


# @router.delete("/me")
# async def delete_user(
#     current_user: User = Security(get_current_user),
#     user_service: UserService = Depends(get_user_service),
#     session: AsyncSession = Depends(get_db_session),
# ) -> None:
#     await user_service.delete(current_user.id, session)
