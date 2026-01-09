from pydantic import BaseModel, Field


class AssistanceBaseSchema(BaseModel):
    name: str = Field(min_length=2, max_length=30, examples=["Haircut"])
    price: int = Field(gt=0, examples=[500])
    duration_minutes: int = Field(gt=0, examples=[20])
    description: str | None = Field(
        default=None,
        examples=[
            "Professional men's haircut tailored to the client's head shape, hair type, and personal style."
        ],
    )

    class Config:
        from_attributes = True


class AssistanceSchema(AssistanceBaseSchema):
    id: int


class AssistanceCreateSchema(AssistanceBaseSchema):
    pass


class AssistanceUpdateSchema(BaseModel):
    name: str | None = Field(
        default=None, min_length=2, max_length=30, examples=["Haircut"]
    )
    price: int | None = Field(default=None, gt=0, examples=[500])
    duration_minutes: int | None = Field(default=None, gt=0, examples=[20])
    description: str | None = Field(default=None, examples=["Professional haircut"])
