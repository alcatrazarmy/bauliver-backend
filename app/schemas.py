from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    role: Optional[str] = "user"
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Permit Schemas
class PermitBase(BaseModel):
    customer_name: str
    address: str
    system_size_kw: Optional[Decimal] = None
    status: Optional[str] = "pending"
    pdf_url: Optional[str] = None


class PermitCreate(PermitBase):
    pass


class PermitUpdate(BaseModel):
    customer_name: Optional[str] = None
    address: Optional[str] = None
    system_size_kw: Optional[Decimal] = None
    status: Optional[str] = None
    pdf_url: Optional[str] = None


class Permit(PermitBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
