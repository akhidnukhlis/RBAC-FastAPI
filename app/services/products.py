from sqlalchemy.orm import Session
from app.repositories.products import create_product
from app.schemas.products import ProductCreate

def create_new_product(db: Session, product: ProductCreate):
    return create_product(db, product)
