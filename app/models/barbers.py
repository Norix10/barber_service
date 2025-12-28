from sqlalchemy import String, Integer, Enum, Float, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.schemas.enum.barbers import BarberDivision


class Barbers(Base):
    __tablename__ = "barbers"

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(13), nullable=False, unique=True)
    division: Mapped[BarberDivision] = mapped_column(
        Enum(BarberDivision), nullable=False, default=BarberDivision.barber
    )
    is_free: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=0)

    appointments = relationship(
        "Appointment", back_populates="barber", cascade="all, delete-orphan"
    )
