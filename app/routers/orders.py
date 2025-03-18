from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.orders import OrderCreate, Order
from app.repositories.orders import create_order
from app.middleware.permission_middleware import PermissionMiddleware
from app.middleware.auth_middleware import AuthMiddleware

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(7))], response_model=Order)
def create_new_order(request: Request, order: OrderCreate, db: Session = Depends(get_db)):
    tenant = request.headers.get("X-Tenant")
    if tenant:
        db.execute(f"SET search_path TO {tenant}")

    return create_order(db, order)