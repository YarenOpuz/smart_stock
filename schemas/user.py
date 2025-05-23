from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    office_address: Optional[str] = None
    phone_number: Optional[str] = None
  


class UserRead(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    office_address: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None