from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.product import Product
from models.warehouse import Warehouse
from schemas.product import ProductCreate, ProductRead
from routers.auth import get_current_user

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check if warehouse exists
    warehouse = db.query(Warehouse).filter(Warehouse.id == product_data.warehouse_id).first()
    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {product_data.warehouse_id} not found"
        )
    
    # Create new product
    new_product = Product(**product_data.dict())
    
    # Add to database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product


@router.get("/", response_model=List[ProductRead])
async def get_products(
    skip: int = 0, 
    limit: int = 100, 
    warehouse_id: int = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Filter by warehouse if warehouse_id is provided
    if warehouse_id:
        products = db.query(Product).filter(
            Product.warehouse_id == warehouse_id
        ).offset(skip).limit(limit).all()
    else:
        products = db.query(Product).offset(skip).limit(limit).all()
    
    return products


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int, 
    product_data: ProductCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Find product
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    # Check if warehouse exists if changing warehouse
    if product_data.warehouse_id != product.warehouse_id:
        warehouse = db.query(Warehouse).filter(Warehouse.id == product_data.warehouse_id).first()
        if not warehouse:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Warehouse with ID {product_data.warehouse_id} not found"
            )
    
    # Update product
    for key, value in product_data.dict().items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Find product
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    # Delete product
    db.delete(product)
    db.commit()
    
    return None 