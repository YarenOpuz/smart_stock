from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models.warehouse import Warehouse
from schemas.warehouse import WarehouseCreate, WarehouseRead
from routers.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/warehouses", tags=["warehouses"])


@router.post("/", response_model=WarehouseRead, status_code=status.HTTP_201_CREATED)
def create_warehouse(
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Create new warehouse with all fields from schema
    new_warehouse = Warehouse(
        name=warehouse.name,
        location=warehouse.location,
        capacity=warehouse.capacity,
        rental_price=warehouse.rental_price,
        warehouse_type=warehouse.warehouse_type,
        used_by_company=warehouse.used_by_company,
        is_available=warehouse.is_available,
        owner_id=current_user.id  # Set the owner to current user
    )
    
    # Add to database
    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)
    
    return new_warehouse


@router.get("/", response_model=List[WarehouseRead])
def list_warehouses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    warehouses = db.query(Warehouse).offset(skip).limit(limit).all()
    return warehouses


@router.get("/{warehouse_id}", response_model=WarehouseRead)
def get_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse


@router.put("/{warehouse_id}", response_model=WarehouseRead)
def update_warehouse(
    warehouse_id: int,
    warehouse_update: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get warehouse
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    # Update all warehouse fields from the update data
    for field, value in warehouse_update.dict().items():
        setattr(warehouse, field, value)
    
    # Save changes
    db.commit()
    db.refresh(warehouse)
    
    return warehouse


@router.delete("/{warehouse_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get warehouse
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    # Delete warehouse
    db.delete(warehouse)
    db.commit()
    
    return None 