from datetime import datetime

from pydantic import validator, EmailStr, BaseModel

from project.base.schema import BaseSchema
from project.config import PASSWORD_ENCRYPTION, TOKEN_TYPE


class UserSchema(BaseSchema):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    last_login: datetime = None


class TokenSchema(BaseModel):
    type: str = TOKEN_TYPE
    token: str


class SignUpSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password: str

    @validator('email')
    def trim_label(cls, v):
        return v.strip()

    @validator('username')
    def trim_color(cls, v):
        return v.strip()

    @validator('password')
    def trim_password(cls, v):
        return PASSWORD_ENCRYPTION.hash(v)


class LogInSchema(BaseModel):
    username: str
    password: str


class LogInResponseSchema(BaseModel):
    token: TokenSchema
    user: UserSchema
