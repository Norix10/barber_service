# app/repositories/appointments.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from datetime import datetime, timedelta
from app.models.appointments import Appointment
from app.schemas.appointments import AppointmentSchema
from app.schemas.enum.appointments import AppointmentsEnum


class AppointmentRepository:
    @staticmethod
    async def get_by_id(appoint_id: int, session: AsyncSession):
        return await session.get(Appointment, appoint_id)

    @staticmethod
    async def add(appointment: Appointment, session: AsyncSession) -> Appointment:
        session.add(appointment)
        await session.commit()
        await session.refresh(appointment)
        return appointment

    @staticmethod
    async def list(user_id: int, session: AsyncSession) -> list[Appointment]:
        result = await session.execute(
            select(Appointment).where(Appointment.user_id == user_id)
        )
        appointments = result.scalars().all()
        return list(appointments)

    @staticmethod
    async def check_barber_availability(
        barber_id: int,
        appointment_datetime: datetime,
        duration_minutes: int,
        session: AsyncSession,
        exclude_appointment_id: int | None = None,  # ← Новий параметр
    ) -> bool:
        end_time = appointment_datetime + timedelta(minutes=duration_minutes)

        # Базові умови
        conditions = [
            Appointment.barber_id == barber_id,
            Appointment.status.in_(
                [AppointmentsEnum.pending, AppointmentsEnum.verified]
            ),
            or_(
                and_(
                    Appointment.appointment_datetime <= appointment_datetime,
                    Appointment.appointment_datetime
                    + timedelta(minutes=duration_minutes)
                    > appointment_datetime,
                ),
                and_(
                    Appointment.appointment_datetime < end_time,
                    Appointment.appointment_datetime
                    + timedelta(minutes=duration_minutes)
                    >= end_time,
                ),
                and_(
                    Appointment.appointment_datetime >= appointment_datetime,
                    Appointment.appointment_datetime
                    + timedelta(minutes=duration_minutes)
                    <= end_time,
                ),
            ),
        ]

        # Виключаємо поточний appointment (якщо це update)
        if exclude_appointment_id is not None:
            conditions.append(Appointment.id != exclude_appointment_id)

        result = await session.execute(select(Appointment).where(and_(*conditions)))

        conflicting_appointment = result.scalar_one_or_none()
        return conflicting_appointment is None

    @staticmethod
    async def check_user_availability(
        user_id: int,
        appointment_datetime: datetime,
        duration_minutes: int,
        session: AsyncSession,
        exclude_appointment_id: int | None = None,  # ← Новий параметр
    ) -> bool:
        end_time = appointment_datetime + timedelta(minutes=duration_minutes)

        # Базові умови
        conditions = [
            Appointment.user_id == user_id,
            Appointment.status == AppointmentsEnum.pending,
            or_(
                and_(
                    Appointment.appointment_datetime <= appointment_datetime,
                    Appointment.appointment_datetime
                    + timedelta(minutes=duration_minutes)
                    > appointment_datetime,
                ),
                and_(
                    Appointment.appointment_datetime < end_time,
                    Appointment.appointment_datetime
                    + timedelta(minutes=duration_minutes)
                    >= end_time,
                ),
                and_(
                    Appointment.appointment_datetime >= appointment_datetime,
                    Appointment.appointment_datetime
                    + timedelta(minutes=duration_minutes)
                    <= end_time,
                ),
            ),
        ]

        # Виключаємо поточний appointment (якщо це update)
        if exclude_appointment_id is not None:
            conditions.append(Appointment.id != exclude_appointment_id)

        result = await session.execute(select(Appointment).where(and_(*conditions)))

        conflicting_appointment = result.scalar_one_or_none()
        return conflicting_appointment is None

    @staticmethod
    async def check_user_duplicate(
        user_id: int,
        barber_id: int,
        service_id: int,
        appointment_datetime: datetime,
        session: AsyncSession,
        exclude_appointment_id: int | None = None,  # ← Новий параметр
    ) -> bool:
        # Базові умови
        conditions = [
            Appointment.user_id == user_id,
            Appointment.barber_id == barber_id,
            Appointment.service_id == service_id,
            Appointment.appointment_datetime == appointment_datetime,
            Appointment.status == AppointmentsEnum.pending,
        ]

        # Виключаємо поточний appointment (якщо це update)
        if exclude_appointment_id is not None:
            conditions.append(Appointment.id != exclude_appointment_id)

        result = await session.execute(select(Appointment).where(and_(*conditions)))

        duplicate = result.scalar_one_or_none()
        return duplicate is None

    @staticmethod
    async def get_all(session: AsyncSession):
        result = await session.execute(select(Appointment))
        appointments = result.scalars().all()
        return [
            AppointmentSchema.model_validate(appointment, from_attributes=True)
            for appointment in appointments
        ]

    @staticmethod
    async def update(appoint: Appointment, session: AsyncSession):
        session.add(appoint)
        await session.commit()
        await session.refresh(appoint)
        return appoint

    @staticmethod
    async def delete(appoint: Appointment, session: AsyncSession) -> None:
        await session.delete(appoint)
        await session.commit()
