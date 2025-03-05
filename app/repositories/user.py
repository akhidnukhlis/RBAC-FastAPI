from sqlalchemy.orm import Session
from app import schemas, models
from app.core import security


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=str(user.email),
        hashed_password=hashed_password,
        role_id=user.role_id
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None

    db_user.username = user.username
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    if not security.verify_password(password, str(user.hashed_password)):
        return None
    return user

def get_user_by_access_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.access_token == token, models.User.is_active == True).first()

def update_user_token(db: Session, user_id: int, token: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.access_token = token
        db.commit()
        db.refresh(user)