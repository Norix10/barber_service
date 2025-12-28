from pydantic import BaseModel, EmailStr, Field


class AdminBaseSchema(BaseModel):
    name: str = Field(min_length=2, max_length=30, examples=["Admin Name"])
    email: EmailStr = Field(examples=["admin@example.com"])

    class Config:
        from_attributes = True


class AdminSchema(AdminBaseSchema):
    id: int


class AdminCreateSchema(AdminBaseSchema):
    password: str = Field(min_length=8, examples=["Str1ngst!"])


class AdminSignInSchema(BaseModel):
    email: EmailStr = Field(examples=["admin@example.com"])
    password: str = Field(min_length=8, examples=["Str1ngst!"])


class AdminUpdateSchema(BaseModel):
    name: str | None = Field(
        default=None, min_length=2, max_length=30, examples=["Admin Name"]
    )
    email: EmailStr | None = Field(default=None, examples=["admin@example.com"])
    password: str | None = Field(default=None, min_length=8, examples=["Str1ngst!"])
