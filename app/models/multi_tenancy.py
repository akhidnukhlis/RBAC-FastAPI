from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, ForeignKey
from sqlalchemy.sql import func
from app.models.base import TenantMixin
from app.core.database import Base

class Note(Base, TenantMixin):
    __tablename__ = "notes"
    __tenant_schema__ = "tenant_schema"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by = Column(String(255), nullable=True)

class Order(Base, TenantMixin):
    __tablename__ = 'orders'
    __tenant_schema__ = "tenant_schema"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("public.users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey(f"{__tenant_schema__}.products.id"), nullable=False)
    note_id = Column(Integer, ForeignKey(f"{__tenant_schema__}.notes.id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by = Column(String(255), nullable=True)