from sqlalchemy.orm import Session
from app.models.product import Product

def create_product(db: Session, product_data):
    db_product = Product(**product_data.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product