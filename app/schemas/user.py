from pydantic import BaseModel, EmailStr, Field

class UserBaseSchema(BaseModel):
    name: str = Field(min_length=2, max_length=30, examples=["Andriy Vorobei"])
    email: EmailStr = Field(examples=["adnr.krv@example.com"])

class UserSchema(UserBaseSchema):
    id: int

class UserSignInSchema(BaseModel):
    email: EmailStr = Field(examples=["adnr.krv@example.com"])
    password: str = Field(min_length=8, examples=["Str1ngst!"]) 

class UserSignUpSchema(UserBaseSchema):
    id: int | None = None
    password: str = Field(min_length=8, examples=["Str1ngst!"])

class UserUpdateSchema(BaseModel):
    name: str = Field(min_length=2, max_length=30, examples=["Andriy Vorobei"])
    password: str = Field(min_length=8, examples=["Str1ngst!"]) 