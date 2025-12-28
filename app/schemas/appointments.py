from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.schemas.enum.appointments import AppointmentsEnum


class AppointmentBaseSchema(BaseModel):
    user_id: int = Field(examples=[1])
    barber_id: int = Field(examples=[1])
    service_id: int = Field(examples=[1])
    appointment_datetime: datetime = Field(examples=["2025-12-26T14:30:00"])
    status: AppointmentsEnum = Field(default=AppointmentsEnum.pending)
    notes: str | None = Field(
        default=None, max_length=500, examples=["Special instructions"]
    )

    class Config:
        from_attributes = True


class AppointmentSchema(AppointmentBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class AppointmentCreateSchema(BaseModel):
    barber_id: int = Field(examples=[1])
    service_id: int = Field(examples=[1])
    appointment_datetime: datetime = Field(examples=["2025-12-26T14:30:00"])
    notes: str | None = Field(
        default=None, max_length=500, examples=["Special instructions"]
    )


class AppointmentUpdateSchema(BaseModel):
    appointment_datetime: datetime | None = Field(
        default=None, examples=["2025-12-26T14:30:00"]
    )
    status: AppointmentsEnum | None = Field(
        default=None, examples=[AppointmentsEnum.cancelled]
    )
    notes: str | None = Field(
        default=None, max_length=500, examples=["Special instructions"]
    )
