from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
import datetime
from app.models.base import Base, TenantMixin

class Note(Base, TenantMixin):
    __tablename__ = "notes"
    __table_args__ = {"schema": "tenant_schema"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Order(Base, TenantMixin):
    __tablename__ = 'orders'
    __table_args__ = {"schema": "tenant_schema"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("public.users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("tenant_schema.products.id"), nullable=False)
    note_id = Column(Integer, ForeignKey("tenant_schema.notes.id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)