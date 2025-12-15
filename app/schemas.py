from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
email: EmailStr
password: str
role: str | None = None


class UserOut(BaseModel):
id: int
email: EmailStr
role: str
is_active: bool


class Config:
orm_mode = True


class Token(BaseModel):
access_token: str
token_type: str
