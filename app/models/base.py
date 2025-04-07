from sqlalchemy.ext.declarative import declared_attr

class TenantMixin:
    @declared_attr
    def __table_args__(cls):
        return {"schema": cls.__tenant_schema__}