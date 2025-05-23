from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.warehouse import Warehouse
from schemas.warehouse import WarehouseCreate, WarehouseRead
from routers.auth import get_current_user

router = APIRouter(prefix="/warehouses", tags=["warehouses"])


@router.post("/", response_model=WarehouseRead, status_code=status.HTTP_201_CREATED)
async def create_warehouse(
    warehouse_data: WarehouseCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check if warehouse with this name already exists
    existing_warehouse = db.query(Warehouse).filter(Warehouse.name == warehouse_data.name).first()
    if existing_warehouse:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Warehouse with name '{warehouse_data.name}' already exists"
        )
    
    # Create new warehouse
    new_warehouse = Warehouse(**warehouse_data.dict())
    
    # Add to database
    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)
    
    return new_warehouse


@router.get("/", response_model=List[WarehouseRead])
async def get_warehouses(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    warehouses = db.query(Warehouse).offset(skip).limit(limit).all()
    return warehouses


@router.get("/{warehouse_id}", response_model=WarehouseRead)
async def get_warehouse(
    warehouse_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if warehouse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {warehouse_id} not found"
        )
    return warehouse


@router.put("/{warehouse_id}", response_model=WarehouseRead)
async def update_warehouse(
    warehouse_id: int, 
    warehouse_data: WarehouseCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Find warehouse
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if warehouse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {warehouse_id} not found"
        )
    
    # Check if updating name to an existing name
    if warehouse.name != warehouse_data.name:
        existing_warehouse = db.query(Warehouse).filter(Warehouse.name == warehouse_data.name).first()
        if existing_warehouse:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Warehouse with name '{warehouse_data.name}' already exists"
            )
    
    # Update warehouse
    for key, value in warehouse_data.dict().items():
        setattr(warehouse, key, value)
    
    db.commit()
    db.refresh(warehouse)
    
    return warehouse


@router.delete("/{warehouse_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_warehouse(
    warehouse_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Find warehouse
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if warehouse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {warehouse_id} not found"
        )
    
    # Delete warehouse
    db.delete(warehouse)
    db.commit()
    
    return None 