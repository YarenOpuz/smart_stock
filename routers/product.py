from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from database import get_db
from models.product import Product
from models.warehouse import Warehouse
from schemas.product import ProductCreate, ProductRead
from routers.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/products", tags=["products"])


class ProductTransfer(BaseModel):
    product_id: int
    from_warehouse_id: int
    to_warehouse_id: int
    quantity: int


@router.post("/transfer", response_model=ProductRead)
def transfer_product(
    transfer: ProductTransfer,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if source warehouse exists and has the product
    source_product = db.query(Product).filter(
        Product.id == transfer.product_id,
        Product.warehouse_id == transfer.from_warehouse_id
    ).first()
    
    if not source_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product not found in source warehouse"
        )
    
    # Check if there's enough quantity
    if source_product.quantity < transfer.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough quantity in source warehouse"
        )
    
    # Check if target warehouse exists
    target_warehouse = db.query(Warehouse).filter(
        Warehouse.id == transfer.to_warehouse_id
    ).first()
    
    if not target_warehouse:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Target warehouse not found"
        )
    
    # Check if product with same name and description exists in target warehouse
    target_product = db.query(Product).filter(
        Product.warehouse_id == transfer.to_warehouse_id,
        Product.name == source_product.name,
        Product.description == source_product.description
    ).first()
    
    # Update source product quantity
    source_product.quantity -= transfer.quantity
    
    if target_product:
        # Update existing product quantity
        target_product.quantity += transfer.quantity
        result_product = target_product
    else:
        # Create new product in target warehouse
        new_product = Product(
            name=source_product.name,
            description=source_product.description,
            quantity=transfer.quantity,
            warehouse_id=transfer.to_warehouse_id,
            is_active=True
        )
        db.add(new_product)
        result_product = new_product
    
    # Save changes
    db.commit()
    db.refresh(result_product)
    
    return result_product


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if warehouse exists
    warehouse = db.query(Warehouse).filter(Warehouse.id == product.warehouse_id).first()
    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Warehouse not found"
        )
    
    # Create new product
    new_product = Product(**product.dict())
    
    # Add to database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product


@router.get("/", response_model=List[ProductRead])
def list_products(
    skip: int = 0,
    limit: int = 100,
    warehouse_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Product)
    if warehouse_id:
        query = query.filter(Product.warehouse_id == warehouse_id)
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_update: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get product
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if new warehouse exists
    if product_update.warehouse_id != product.warehouse_id:
        warehouse = db.query(Warehouse).filter(Warehouse.id == product_update.warehouse_id).first()
        if not warehouse:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Warehouse not found"
            )
    
    # Update product fields
    for field, value in product_update.dict().items():
        setattr(product, field, value)
    
    # Save changes
    db.commit()
    db.refresh(product)
    
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get product
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Delete product
    db.delete(product)
    db.commit()
    
    return None 