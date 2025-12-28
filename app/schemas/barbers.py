from pydantic import BaseModel, EmailStr, Field
from app.schemas.enum.barbers import BarberDivision


class BarberBaseSchema(BaseModel):
    name: str = Field(min_length=2, max_length=30, examples=["Andriy Vorobei"])
    email: EmailStr = Field(examples=["barber@example.com"])
    phone_number: str | None = Field(
        default=None, min_length=10, max_length=13, examples=["+380981234567"]
    )
    division: BarberDivision = Field(default=BarberDivision.barber)
    is_free: bool = Field(default=True)
    rating: float = Field(default=0)

    class Config:
        from_attributes = True


class BarberSchema(BarberBaseSchema):
    id: int


class BarberCreateSchema(BarberBaseSchema):
    id: int | None = None
    password: str = Field(min_length=8, examples=["Str1ngst!"])


class BarberSignInSchema(BaseModel):
    email: EmailStr = Field(examples=["barber@example.com"])
    password: str = Field(min_length=8, examples=["Str1ngst!"])


class BarberUpdateSchema(BaseModel):
    name: str | None = Field(
        default=None, min_length=2, max_length=30, examples=["Andriy Vorobei"]
    )
    email: EmailStr | None = Field(default=None, examples=["barber@example.com"])
    phone_number: str | None = Field(
        default=None, min_length=10, max_length=13, examples=["+380981234567"]
    )
    division: BarberDivision | None = Field(default=None)
    is_free: bool | None = Field(default=None)
    rating: float | None = Field(default=None)
    password: str | None = Field(default=None, min_length=8, examples=["Str1ngst!"])
