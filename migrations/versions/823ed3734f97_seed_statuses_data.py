"""seed_statuses_data

Revision ID: 823ed3734f97
Revises: d8a51b5681c3
Create Date: 2026-02-02 13:45:38.278499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '823ed3734f97'
down_revision: Union[str, None] = 'd8a51b5681c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

def upgrade() -> None:
    # Definisi tabel sementara untuk operasi bulk_insert
    statuses_table = table('statuses',
        column('id', Integer),
        column('name', String),
        column('description', String)
    )

    op.bulk_insert(statuses_table,
        [
            {"id": 1, "name": "PENDING_EMAIL_VERIFICATION", "description": "User registered, waiting for email verification"},
            {"id": 2, "name": "PENDING_ADMIN_APPROVAL", "description": "User verified email, waiting for admin approval"},
            {"id": 3, "name": "ACTIVE", "description": "User active, approved, and able to login"},
            {"id": 4, "name": "REJECTED", "description": "User registration rejected by admin"},
            {"id": 5, "name": "BANNED", "description": "User banned or suspended"},
        ]
    )


def downgrade() -> None:
    op.execute("DELETE FROM statuses WHERE id IN (1, 2, 3, 4, 5)")
