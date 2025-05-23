from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int
    warehouse_id: int


class ProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    quantity: int
    is_active: bool
    created_at: datetime
    warehouse_id: int

    class Config:
        orm_mode = True 