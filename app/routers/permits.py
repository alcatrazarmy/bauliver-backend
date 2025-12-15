from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/api/permits", tags=["permits"])


@router.post("/", response_model=schemas.Permit, status_code=status.HTTP_201_CREATED)
def create_permit(
    permit_in: schemas.PermitCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Create a new permit.
    Requires JWT authentication.
    """
    db_permit = models.Permit(
        customer_name=permit_in.customer_name,
        address=permit_in.address,
        system_size_kw=permit_in.system_size_kw,
        status=permit_in.status,
        pdf_url=permit_in.pdf_url,
        user_id=current_user.id
    )
    db.add(db_permit)
    db.commit()
    db.refresh(db_permit)
    
    return db_permit


@router.get("/", response_model=List[schemas.Permit])
def list_permits(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    List all permits.
    - Regular users see only their own permits
    - Admin users see all permits
    """
    if current_user.role == "admin":
        permits = db.query(models.Permit).all()
    else:
        permits = db.query(models.Permit).filter(
            models.Permit.user_id == current_user.id
        ).all()
    
    return permits


@router.get("/{permit_id}", response_model=schemas.Permit)
def get_permit(
    permit_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Get a single permit by ID.
    Users can only view their own permits unless they are admin.
    """
    permit = db.query(models.Permit).filter(models.Permit.id == permit_id).first()
    
    if not permit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permit not found"
        )
    
    # Check permissions: user can only view their own permits unless admin
    if current_user.role != "admin" and permit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this permit"
        )
    
    return permit


@router.put("/{permit_id}", response_model=schemas.Permit)
def update_permit(
    permit_id: int,
    permit_update: schemas.PermitUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Update a permit.
    Users can only update their own permits unless they are admin.
    """
    permit = db.query(models.Permit).filter(models.Permit.id == permit_id).first()
    
    if not permit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permit not found"
        )
    
    # Check permissions: user can only update their own permits unless admin
    if current_user.role != "admin" and permit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this permit"
        )
    
    # Update only provided fields
    update_data = permit_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(permit, field, value)
    
    db.commit()
    db.refresh(permit)
    
    return permit


@router.delete("/{permit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permit(
    permit_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Delete a permit.
    Users can only delete their own permits unless they are admin.
    """
    permit = db.query(models.Permit).filter(models.Permit.id == permit_id).first()
    
    if not permit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permit not found"
        )
    
    # Check permissions: user can only delete their own permits unless admin
    if current_user.role != "admin" and permit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this permit"
        )
    
    db.delete(permit)
    db.commit()
