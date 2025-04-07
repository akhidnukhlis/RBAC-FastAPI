from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas import TenantsCreate
from app.repositories import tenants as tenants_repository

def add_tenants(db: Session, tenants: TenantsCreate):
    new_role = tenants_repository.create_tenants(db, tenants)

    if not new_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    return new_role