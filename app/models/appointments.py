from datetime import datetime
from sqlalchemy import String, Enum, DateTime, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.schemas.enum.appointments import AppointmentsEnum


class Appointment(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    barber_id: Mapped[int] = mapped_column(ForeignKey("barbers.id"), nullable=False)
    assistance_id: Mapped[int] = mapped_column(ForeignKey("assistances.id"), nullable=False)

    appointment_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[AppointmentsEnum] = mapped_column(
        Enum(AppointmentsEnum), nullable=False, default=AppointmentsEnum.pending
    )
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user = relationship("User", back_populates="appointments")
    barber = relationship("Barbers", back_populates="appointments")
    assistance = relationship("Assistance", back_populates="appointments")
