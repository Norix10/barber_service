from fastapi import APIRouter, Depends, Security

from app.db.database import get_db_session, AsyncSession
from app.models.user import User
from app.models.admin import Admin
from app.models.appointments import Appointment
from app.schemas.appointments import (
    AppointmentBaseSchema,
    AppointmentCreateSchema,
    AppointmentSchema,
    AppointmentUpdateSchema,
)
from app.services.appointments import AppointmentService, get_appointments_service
from app.auth.universal_jwt import get_current_user, get_current_admin

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/create", response_model=AppointmentSchema)
async def create(
    data: AppointmentCreateSchema,
    current_user: User = Security(get_current_user),
    appoint_service: AppointmentService = Depends(get_appointments_service),
    session: AsyncSession = Depends(get_db_session),
) -> Appointment:
    data = data.model_copy(update={"user_id": current_user.id})
    return await appoint_service.create(data, session)


@router.get("/my-list")
async def get_my_appointments(
    current_user: User = Security(get_current_user),
    appoint_service: AppointmentService = Depends(get_appointments_service),
    session: AsyncSession = Depends(get_db_session),
):
    return await appoint_service.get_list(current_user.id, session)


@router.get("/get-all")
async def get_all(
    current_admin: Admin = Security(get_current_admin),
    appoint_service: AppointmentService = Depends(get_appointments_service),
    session: AsyncSession = Depends(get_db_session),
):
    return await appoint_service.get_all(session)


@router.patch("/update/{appoint_id}", response_model=AppointmentSchema)
async def update(
    appoint_id: int,
    data: AppointmentUpdateSchema,
    current_user: User = Security(get_current_user),
    appoint_service: AppointmentService = Depends(get_appointments_service),
    session: AsyncSession = Depends(get_db_session),
):
    return await appoint_service.update(
        appoint_id=appoint_id, user_id=current_user.id, data=data, session=session
    )


@router.delete("/delete/{appoint_id}", status_code=204)
async def delete(
    appoint_id: int,
    current_user: User = Security(get_current_user),
    appoint_service: AppointmentService = Depends(get_appointments_service),
    session: AsyncSession = Depends(get_db_session),
) -> None:
    await appoint_service.delete(appoint_id, current_user.id, session)
