from pydantic import BaseModel
from datetime import datetime


class WarehouseCreate(BaseModel):
    name: str
    location: str
    capacity: int


class WarehouseRead(BaseModel):
    id: int
    name: str
    location: str
    capacity: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True