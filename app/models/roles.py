from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)