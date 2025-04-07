from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by = Column(String(255), nullable=True)