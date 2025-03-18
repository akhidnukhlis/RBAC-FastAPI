from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.core.database import get_db
from app.services import users as user_service
from app.schemas.users import UserLogin, UserResponse

router = APIRouter(tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_create = schemas.UserCreate(
        email=user.email,
        username=user.username,
        password=user.password
    )

    return user_service.register_user(db, user_create)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    token_response = user_service.login_user(db, user)

    if not token_response:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return token_response