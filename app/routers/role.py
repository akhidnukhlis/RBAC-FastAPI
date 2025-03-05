from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.services.role as role_service
from app.schemas import RoleResponse, RoleCreate
from app.core.database import get_db

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return role_service.add_role(db=db, role=role)

@router.get("/", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return role_service.fetch_all_role(db)
