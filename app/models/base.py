from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TenantMixin:
    __table_args__ = {"schema": None}
