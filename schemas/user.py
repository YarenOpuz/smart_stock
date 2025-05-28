from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi import UploadFile



class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    office_address: Optional[str] = None
    phone_number: Optional[str] = None
    user_type: str
    image: Optional[UploadFile] = None 
  


class UserRead(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    office_address: Optional[str] = None
    phone_number: Optional[str] = None
    image_path: Optional[str] = None
    user_type: str


    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None