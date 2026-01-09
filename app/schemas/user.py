from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    name: str = Field(min_length=2, max_length=30, examples=["Andriy Vorobei"])
    email: EmailStr = Field(examples=["user@example.com"])

    class Config:
        from_attributes = True


class UserSchema(UserBaseSchema):
    id: int


class UserCreateSchema(UserBaseSchema):
    password: str = Field(min_length=8, examples=["Str1ngst!"])


class UserSignInSchema(BaseModel):
    email: EmailStr = Field(examples=["user@example.com"])
    password: str = Field(min_length=8, examples=["Str1ngst!"])


class UserUpdateSchema(BaseModel):
    name: str | None = Field(
        default=None, min_length=2, max_length=30, examples=["Andriy Vorobei"]
    )
    password: str | None = Field(default=None, min_length=8, examples=["Str1ngst!"])
