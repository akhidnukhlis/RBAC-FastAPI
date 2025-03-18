from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.services.roles as role_service
from app.schemas import RoleResponse, RoleCreate
from app.core.database import get_db
from app.middleware.permission_middleware import PermissionMiddleware
from app.middleware.auth_middleware import AuthMiddleware

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(7))], response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return role_service.add_role(db=db, role=role)

@router.get("/", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(8))], response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return role_service.fetch_all_role(db)
