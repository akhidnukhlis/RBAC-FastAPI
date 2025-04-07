from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.services.tenants as tenants_service
from app.schemas import TenantsResponse, TenantsCreate
from app.core.database import get_db
from app.middleware.permission_middleware import PermissionMiddleware
from app.middleware.auth_middleware import AuthMiddleware

router = APIRouter(prefix="/tenants", tags=["Tenants"])

@router.post("/", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(7))], response_model=TenantsResponse)
def create_tenants(tenants: TenantsCreate, db: Session = Depends(get_db)):
    return tenants_service.add_tenants(db=db, tenants=tenants)