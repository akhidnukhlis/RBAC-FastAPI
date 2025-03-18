from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.products import ProductCreate, Product
from app.services.products import create_new_product
from app.middleware.permission_middleware import PermissionMiddleware
from app.middleware.auth_middleware import AuthMiddleware

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", dependencies=[Depends(AuthMiddleware), Depends(PermissionMiddleware(7))], response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_new_product(db, product)
