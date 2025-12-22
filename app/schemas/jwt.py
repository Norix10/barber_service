from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    sub: str

class AccessTokenOnly(BaseModel):
    access_token: str

class FullTokenInfo(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str