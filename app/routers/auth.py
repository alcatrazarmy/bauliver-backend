from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas import UserCreate, Token, UserOut
from app.models import User
from app.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, get_current_user


router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
existing_user = db.query(User).filter(User.email == user_in.email).first()
if existing_user:
raise HTTPException(status_code=400, detail="Email already registered")


user = User(
email=user_in.email,
hashed_password=get_password_hash(user_in.password),
role=user_in.role or "user",
is_active=True
)
db.add(user)
db.commit()
db.refresh(user)
return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
user = db.query(User).filter(User.email == form_data.username).first()
if not user or not verify_password(form_data.password, user.hashed_password):
raise HTTPException(status_code=401, detail="Invalid credentials")


token = create_access_token({"sub": user.email})
return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
return current_user
