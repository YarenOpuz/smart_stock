from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import User
from schemas.warehouse import WarehouseRead
from routers.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}/warehouses", response_model=List[WarehouseRead])
def get_user_warehouses(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find user
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Return user's warehouses
    return user.warehouses 