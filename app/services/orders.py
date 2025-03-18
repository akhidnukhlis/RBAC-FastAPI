from sqlalchemy.orm import Session
from app.repositories.orders import create_order
from app.schemas.orders import OrderCreate

def create_new_order(db: Session, order: OrderCreate, tenant: str):
    db.execute(f"SET search_path TO {tenant}")
    return create_order(db, order)
