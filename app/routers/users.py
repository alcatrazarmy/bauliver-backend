from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=schemas.User)
def get_current_user_profile(
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Get profile information of the currently logged-in user.
    """
    return current_user
