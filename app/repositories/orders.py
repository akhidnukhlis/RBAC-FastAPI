from sqlalchemy.orm import Session
from app.models.multi_tenancy import Order

def create_order(db: Session, order_data):
    db_order = Order(**order_data.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order