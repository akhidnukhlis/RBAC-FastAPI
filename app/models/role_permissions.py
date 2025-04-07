from sqlalchemy import Column, Integer, TIMESTAMP, String
from sqlalchemy.sql import func
from app.core.database import Base

class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, nullable=False)
    permission_id = Column(Integer, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by = Column(String(255), nullable=True)