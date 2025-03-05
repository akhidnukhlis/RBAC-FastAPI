from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, String
from sqlalchemy.sql import func
from app.core.database import Base

class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, nullable=False)
    permission_id = Column(Integer, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_by = Column(String(255), nullable=True)