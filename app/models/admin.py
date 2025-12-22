from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Admin(Base):
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
