from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.repositories.appointments import AppointmentRepository
from app.repositories.barbers import BarbersRepository
from app.repositories.assistance import AssistanceRepository
from app.models.appointments import Appointment
from app.schemas.appointments import (
    AppointmentCreateSchema,
    AppointmentSchema,
    AppointmentUpdateSchema,
)
from app.schemas.enum.appointments import AppointmentsEnum
from app.services.exc.appointments import (
    BarberNotFoundException,
    ServiceNotFoundException,
    AppointmentNotFoundException,
    UserNotAvailableException,
    DuplicateAppointmentException,
    BarberNotAvailableException,
    AppointmentNotOwnedException,
    AppointmentCannotBeUpdatedException,
)
from app.services.exc.base import NotFoundException


class AppointmentService:
    def __init__(self) -> None:
        self._repository = AppointmentRepository()
        self._barber_repository = BarbersRepository()
        self._assistance_repository = AssistanceRepository()

    async def get_appoint_or_error(self, appoint_id: int, session: AsyncSession):
        appoint = await self._repository.get_by_id(appoint_id, session)
        if not appoint:
            raise NotFoundException
        return appoint


    async def _validate_barber_exists(self, barber_id: int, session: AsyncSession):
        barber = await self._barber_repository.get_by_id(barber_id, session)
        if not barber:
            raise BarberNotFoundException(barber_id)
        return barber

    async def _validate_assistance_exists(self, assistance_id: int, session: AsyncSession):
        assistance = await self._assistance_repository.get_by_id(assistance_id, session)
        if not assistance:
            raise ServiceNotFoundException(assistance_id)
        return assistance

    async def _validate_user_availability(
        self,
        user_id: int,
        appointment_datetime: datetime,
        duration_minutes: int,
        session: AsyncSession,
        exclude_appointment_id: int | None = None,
    ):
        user_is_available = await self._repository.check_user_availability(
            user_id=user_id,
            appointment_datetime=appointment_datetime,
            duration_minutes=duration_minutes,
            session=session,
            exclude_appointment_id=exclude_appointment_id,
        )
        if not user_is_available:
            raise UserNotAvailableException(appointment_datetime)

    async def _validate_no_duplicate(
        self,
        user_id: int,
        barber_id: int,
        assistance_id: int,
        appointment_datetime: datetime,
        session: AsyncSession,
    ):
        is_unique = await self._repository.check_user_duplicate(
            user_id=user_id,
            barber_id=barber_id,
            assistance_id=assistance_id,
            appointment_datetime=appointment_datetime,
            session=session,
        )
        if not is_unique:
            raise DuplicateAppointmentException()

    async def _validate_barber_availability(
        self,
        barber_id: int,
        appointment_datetime: datetime,
        duration_minutes: int,
        session: AsyncSession,
        exclude_appointment_id: int | None = None,
    ):
        barber_is_available = await self._repository.check_barber_availability(
            barber_id=barber_id,
            appointment_datetime=appointment_datetime,
            duration_minutes=duration_minutes,
            session=session,
            exclude_appointment_id=exclude_appointment_id,
        )
        if not barber_is_available:
            raise BarberNotAvailableException(appointment_datetime)

    async def _validate_appointment_can_be_updated(self, appointment: Appointment):
        non_updatable_statuses = [
            AppointmentsEnum.cancelled,
            AppointmentsEnum.completed,
        ]
        if appointment.status in non_updatable_statuses:
            raise AppointmentCannotBeUpdatedException(appointment.status.value)

    async def _validate_appointment_ownership(
        self, appointment: Appointment, user_id: int
    ):
        if appointment.user_id != user_id:
            raise AppointmentNotOwnedException()

    async def create(
        self, data: AppointmentCreateSchema, session: AsyncSession
    ) -> Appointment:
        await self._validate_barber_exists(data.barber_id, session)
        assistance = await self._validate_assistance_exists(data.assistance_id, session)
        await self._validate_user_availability(
            user_id=data.user_id,
            appointment_datetime=data.appointment_datetime,
            duration_minutes=assistance.duration_minutes,
            session=session,
        )

        await self._validate_no_duplicate(
            user_id=data.user_id,
            barber_id=data.barber_id,
            assistance_id=data.assistance_id,
            appointment_datetime=data.appointment_datetime,
            session=session,
        )

        await self._validate_barber_availability(
            barber_id=data.barber_id,
            appointment_datetime=data.appointment_datetime,
            duration_minutes=assistance.duration_minutes,
            session=session,
        )

        appointment = Appointment(
            user_id=data.user_id,
            barber_id=data.barber_id,
            assistance_id=data.assistance_id,
            appointment_datetime=data.appointment_datetime,
            notes=data.notes,
        )
        return await self._repository.add(appointment, session)

    async def get_list(self, user_id: int, session: AsyncSession) -> list[Appointment]:
        return await self._repository.list(user_id, session)

    async def get_all(self, session: AsyncSession) -> list[AppointmentSchema]:
        return await self._repository.get_all(session)

    async def update(
        self,
        appoint_id: int,
        user_id: int,
        data: AppointmentUpdateSchema,
        session: AsyncSession,
    ) -> Appointment:
        appoint = await self._repository.get_by_id(appoint_id, session)
        if not appoint:
            raise AppointmentNotFoundException(appoint_id)

        await self._validate_appointment_ownership(appoint, user_id)

        await self._validate_appointment_can_be_updated(appoint)

        # Оновлюємо час (якщо передано)
        if data.appointment_datetime is not None:
            assistance = await self._validate_assistance_exists(appoint.assistance_id, session)

            await self._validate_user_availability(
                user_id=appoint.user_id,
                appointment_datetime=data.appointment_datetime,
                duration_minutes=assistance.duration_minutes,
                session=session,
                exclude_appointment_id=appoint_id,
            )

            await self._validate_barber_availability(
                barber_id=appoint.barber_id,
                appointment_datetime=data.appointment_datetime,
                duration_minutes=assistance.duration_minutes,
                session=session,
                exclude_appointment_id=appoint_id,
            )

            appoint.appointment_datetime = data.appointment_datetime

        if data.status is not None:
            appoint.status = data.status

        if data.notes is not None:
            appoint.notes = data.notes

        return await self._repository.update(appoint, session)


    async def delete(self, appoints: Appointment, session: AsyncSession):
        await self._repository.delete(appoints, session)


    async def update_by_admin(
        self,
        appoint_id: int,
        data: AppointmentUpdateSchema,
        session: AsyncSession
    ) -> Appointment:
        appoint = await self._repository.get_by_id(appoint_id, session)
        if not appoint:
            raise AppointmentNotFoundException(appoint_id)
        
        if data.appointment_datetime is not None:
            assistance = await self._validate_assistance_exists(appoint.assistance_id, session)
            
            await self._validate_user_availability(
                user_id=appoint.user_id,
                appointment_datetime=data.appointment_datetime,
                duration_minutes=assistance.duration_minutes,
                session=session,
                exclude_appointment_id=appoint_id,
            )
            
            await self._validate_barber_availability(
                barber_id=appoint.barber_id,
                appointment_datetime=data.appointment_datetime,
                duration_minutes=assistance.duration_minutes,
                session=session,
                exclude_appointment_id=appoint_id,
            )
            
            appoint.appointment_datetime = data.appointment_datetime
        
        if data.status is not None:
            appoint.status = data.status
        
        if data.notes is not None:
            appoint.notes = data.notes
        
        return await self._repository.update(appoint, session)

async def get_appointments_service() -> AppointmentService:
    return AppointmentService()
