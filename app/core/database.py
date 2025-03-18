from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def create_schema_if_not_exists(schema_name):
    with engine.connect() as conn:
        conn.execute(CreateSchema(schema_name, if_not_exists=True))
        conn.commit()

def get_base(tenant_name: str):
    create_schema_if_not_exists(tenant_name)
    metadata = MetaData(schema=tenant_name)
    Base = declarative_base(metadata=metadata)
    return Base

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()