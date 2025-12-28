from fastapi import APIRouter, Depends, Security

from app.core.config import settings
from app.db.database import AsyncSession, get_db_session
from app.services.admin import AdminService, get_admin_service
from app.services.barbers import BarbersService, get_barbers_service
from app.schemas.admin import (
    AdminBaseSchema,
    AdminSchema,
    AdminSignInSchema,
)
from app.schemas.barbers import (
    BarberBaseSchema,
    BarberSchema,
    BarberSignInSchema,
    BarberCreateSchema,
    BarberUpdateSchema,
)
from app.schemas.jwt import TokenSchema, TokenDataSchema, FullTokenInfo, AccessTokenOnly
from app.models.barbers import Barbers
from app.models.admin import Admin
from app.auth.universal_jwt import get_current_admin


router = APIRouter(prefix="/barbers", tags=["barbers"])


@router.post("/create", response_model=BarberSchema)
async def create(
    data: BarberCreateSchema,
    barber_service: BarbersService = Depends(get_barbers_service),
    current_admin: Admin = Security(get_current_admin),
    session: AsyncSession = Depends(get_db_session),
) -> Barbers:
    return await barber_service.create(data, session)


@router.get("/all-barbers")
async def get_barbers(
    barber_service: BarbersService = Depends(get_barbers_service),
    session: AsyncSession = Depends(get_db_session),
) -> list:
    return await barber_service.get_list(session)


@router.get("/{barber_id}", response_model=BarberSchema)
async def get_barber_by_id(
    barber_id: int,
    barber_service: BarbersService = Depends(get_barbers_service),
    session: AsyncSession = Depends(get_db_session),
):
    barber = await barber_service.get_barber_or_error(barber_id, session)
    return barber


@router.patch("/update/{barber_id}", response_model=BarberSchema)
async def update(
    barber_id: int,
    data: BarberUpdateSchema,
    barber_service: BarbersService = Depends(get_barbers_service),
    current_admin: Admin = Security(get_current_admin),
    session: AsyncSession = Depends(get_db_session),
):
    return await barber_service.update(barber_id, data, session)


@router.delete("/{barber_id}", status_code=204)
async def delete_user(
    barber_id: int,
    barber_service: BarbersService = Depends(get_barbers_service),
    current_admin: Admin = Security(get_current_admin),
    session: AsyncSession = Depends(get_db_session),
) -> None:
    barber = await barber_service.get_barber_or_error(barber_id, session)
    await barber_service.delete(barber, session)


# @router.post("/login", response_model=TokenSchema)
# async def login(
#     data: AdminSignInSchema,
#     session: AsyncSession = Depends(get_db_session),
#     admin_service: AdminService = Depends(get_admin_service),
# ) -> TokenSchema:
#     return await admin_service.authenticate(data, session)


# @router.get("/me", response_model=AdminSchema)
# async def me(current_admin: Admin = Security(get_current_admin)) -> Admin:
#     return current_admin


# @router.get("/all-users", response_model=list)
# async def get_user_list(
#     current_admin: Admin = Security(get_current_admin),
#     session: AsyncSession = Depends(get_db_session),
#     user_service: UserService = Depends(get_user_service),
# ) -> list:
#     return await user_service.get_list(session)


# @router.patch("/user/{user_id}", response_model=UserSchema)
# async def update_user(
#     user_id: int,
#     data: UserUpdateSchemaAdmin,
#     current_admin: Admin = Security(get_current_admin),
#     session: AsyncSession = Depends(get_db_session),
#     user_service: UserService = Depends(get_user_service),
# ) -> UserSchema:
#     return await user_service.update(user_id, data, session)
