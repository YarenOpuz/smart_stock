from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from schemas.product import ProductRead


class WarehouseCreate(BaseModel):
    name: str
    location: str
    capacity: int
    rental_price: float
    warehouse_type: str
    used_by_company: Optional[str] = None
    is_available: Optional[bool] = True


class WarehouseRead(BaseModel):
    id: int
    name: str
    location: str
    capacity: int
    rental_price: float
    warehouse_type: str
    used_by_company: Optional[str] = None
    is_available: bool
    created_at: datetime
    products: List[ProductRead] = []

    class Config:
        orm_mode = True