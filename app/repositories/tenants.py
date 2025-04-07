from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models import Tenant
from app.schemas import TenantsCreate


def create_tenants(db: Session, tenants: TenantsCreate):
    db_tenant = Tenant(name=tenants.name)
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)

    db.execute(text(f"CREATE SCHEMA IF NOT EXISTS {tenants.name}"))
    db.commit()
    return db_tenant