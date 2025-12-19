from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class AdminCreate(BaseModel):
    id: UUID
    name: str
    email: str
    password: str


class AdminResponse(BaseModel):
    id: UUID
    name: str
    email: str

    model_config = {"from_attributes": True}
