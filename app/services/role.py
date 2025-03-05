from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas import RoleCreate
from app.repositories import role as role_repository

def add_role(db: Session, role: RoleCreate):
    new_role = role_repository.create_role(db, role)

    if not new_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    return new_role

def fetch_all_role(db: Session):
    return role_repository.get_roles(db)