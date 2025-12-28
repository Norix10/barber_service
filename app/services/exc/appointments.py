from fastapi import HTTPException, status
from datetime import datetime


class BarberNotFoundException(HTTPException):
    def __init__(self, barber_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Barber with id {barber_id} not found",
        )


class ServiceNotFoundException(HTTPException):
    def __init__(self, service_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service with id {service_id} not found",
        )


class AppointmentNotFoundException(HTTPException):
    def __init__(self, appoint_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with id {appoint_id} not found",
        )


class UserNotAvailableException(HTTPException):
    def __init__(self, appointment_datetime: datetime):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"You already have an appointment at {appointment_datetime}. You cannot be in two places at once!",
        )


class DuplicateAppointmentException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already have an appointment with this barber at this time",
        )


class BarberNotAvailableException(HTTPException):
    def __init__(self, appointment_datetime: datetime):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Barber is not available at {appointment_datetime}. Please choose another time.",
        )


class AppointmentNotOwnedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own appointments",
        )


class AppointmentCannotBeUpdatedException(HTTPException):
    def __init__(self, current_status: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update appointment with status '{current_status}'",
        )
