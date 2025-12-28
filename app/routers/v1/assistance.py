from fastapi import APIRouter, Depends, Security

from app.db.database import get_db_session, AsyncSession
from app.models.services import Service
from app.models.admin import Admin
from app.schemas.assistance import (
    ServiceSchema,
    ServiceCreateSchema,
    ServiceUpdateSchema,
)
from app.services.assistance import AssistanceService, get_assistance_service
from app.auth.universal_jwt import get_current_admin

router = APIRouter(prefix="/assistance", tags=["assistance"])


@router.post("/create", response_model=ServiceSchema)
async def create(
    data: ServiceCreateSchema,
    current_admin: Admin = Security(get_current_admin),
    session: AsyncSession = Depends(get_db_session),
    assist_service: AssistanceService = Depends(get_assistance_service),
):
    return await assist_service.create(data, session)


@router.get("/get-list")
async def get_list(
    session: AsyncSession = Depends(get_db_session),
    assist_service: AssistanceService = Depends(get_assistance_service),
) -> list:
    return await assist_service.get_list(session)


@router.get("/{service_id}", response_model=ServiceSchema)
async def get_by_id(
    service_id: int,
    session: AsyncSession = Depends(get_db_session),
    assist_service: AssistanceService = Depends(get_assistance_service),
):
    return await assist_service.get_assistance_or_erorr(service_id, session)


@router.patch("/update/{service_id}", response_model=ServiceSchema)
async def update(
    service_id: int,
    data: ServiceUpdateSchema,
    assist_service: AssistanceService = Depends(get_assistance_service),
    current_admin: Admin = Security(get_current_admin),
    session: AsyncSession = Depends(get_db_session),
):
    return await assist_service.update(service_id, data, session)


@router.delete("/delete/{service_id}", status_code=204)
async def delete_assist(
    service_id: int,
    assist_service: AssistanceService = Depends(get_assistance_service),
    current_admin: Admin = Security(get_current_admin),
    session: AsyncSession = Depends(get_db_session),
):
    assistance = await assist_service.get_assistance_or_erorr(service_id, session)
    await assist_service.delete(assistance, session)


# @router.post("/signup", response_model=UserSchema)qwe
#     data: UserSignUpSchema,
#     user_service: UserService = Depends(get_user_service),
#     session: AsyncSession = Depends(get_db_session),
# ):
#     return await user_service.create(data, session)


# @router.post("/login", response_model=TokenSchema)
# async def login(
#     data: UserSignInSchema,
#     session: AsyncSession = Depends(get_db_session),
#     user_service: UserService = Depends(get_user_service),
# ) -> TokenSchema:
#     return await user_service.authenticate(data, session)


# @router.get("/me", response_model=UserSchema)
# async def me(current_user: User = Security(get_current_user)) -> User:
#     return current_user


# @router.patch("/me", response_model=UserSchema)
# async def update(
#     data: UserUpdateSchema,
#     current_user: User = Security(get_current_user),
#     user_service: UserService = Depends(get_user_service),
#     session: AsyncSession = Depends(get_db_session),
# ) -> User:
#     return await user_service.update(current_user.id, data, session)
