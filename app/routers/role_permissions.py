from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import RolePermissionCreate, RolePermissionResponse
from app.services import role_permissions
from app.middleware.permission_middleware import PermissionMiddleware
from app.middleware.auth_middleware import AuthMiddleware

router = APIRouter(prefix="/role-permissions", tags=["Role-Permissions"])

@router.post("/", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(1))], response_model=RolePermissionResponse)
def create_role_permission(role_perm: RolePermissionCreate, db: Session = Depends(get_db)):
    new_role_perm = role_permissions.add_role_permission(db, role_perm)

    if not new_role_perm:
        raise HTTPException(status_code=400, detail="Role-Permission already exists")

    return new_role_perm

@router.delete("/", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(6))], response_model=RolePermissionResponse)
def delete_role_permission(role_perm: RolePermissionCreate, db: Session = Depends(get_db)):
    deleted = role_permissions.remove_role_permission(db, role_perm)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role-Permission not found")
    return {"message": "Role-Permission deleted successfully"}

@router.get("/", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(2))], response_model=list[RolePermissionResponse])
def get_all_role_permissions(db: Session = Depends(get_db)):
    return role_permissions.fetch_all_role_permissions(db)
