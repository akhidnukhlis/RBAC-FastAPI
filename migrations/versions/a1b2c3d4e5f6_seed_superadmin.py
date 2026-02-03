"""seed_superadmin

Revision ID: a1b2c3d4e5f6
Revises: fb1c5dc81128
Create Date: 2026-02-02 15:35:00.000000

"""
from typing import Sequence, Union
import uuid
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Boolean, TIMESTAMP
from passlib.context import CryptContext

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'fb1c5dc81128'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    users_table = table('users',
        column('id', String),
        column('email', String),
        column('hashed_password', String),
        column('role_id', Integer),
        column('status_id', Integer),
        column('is_active', Boolean),
        column('created_at', TIMESTAMP),
        column('updated_at', TIMESTAMP)
    )

    # Setup hashing context (Argon2)
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
    
    # Hash the password dynamically
    hashed_pwd = pwd_context.hash("your-super-password")

    op.bulk_insert(users_table,
        [
            {
                "id": str(uuid.uuid4()),
                "email": "superadmin@rbac.com",
                "hashed_password": hashed_pwd,
                "role_id": 1,        # Super Admin
                "status_id": 3,      # Active
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
    )


def downgrade() -> None:
    op.execute("DELETE FROM users WHERE email = 'superadmin@rbac.com'")
