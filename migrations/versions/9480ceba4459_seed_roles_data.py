"""seed_roles_data

Revision ID: 9480ceba4459
Revises: b1a0cef6c9d6
Create Date: 2026-02-02 14:16:45.376902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9480ceba4459'
down_revision: Union[str, None] = 'b1a0cef6c9d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

def upgrade() -> None:
    # Definisi tabel sementara untuk operasi bulk_insert
    roles_table = table('roles',
        column('id', Integer),
        column('name', String),
        column('code', String),
        column('description', String)
    )

    op.bulk_insert(roles_table,
        [
            # Highest Level - Full System Access
            {"id": 1, "name": "Super Administrator", "code": "superadmin", "description": "Has full access to all system features and settings."},
            
            # Management Level
            {"id": 2, "name": "Administrator", "code": "admin", "description": "Can manage users and most content, but limited system config access."},
            {"id": 3, "name": "Manager", "code": "manager", "description": "Can oversee operations, view reports, and manage subordinates."},
            
            # Operational Level
            {"id": 4, "name": "Editor", "code": "editor", "description": "Can create, edit, and publish content."},
            {"id": 5, "name": "Moderator", "code": "moderator", "description": "Can review user content and manage community interactions."},
            {"id": 6, "name": "Support", "code": "support", "description": "Can access user data for troubleshooting and support tickets."},
            
            # End User Level
            {"id": 7, "name": "Standard User", "code": "user", "description": "Regular registered user with standard access."},
            {"id": 8, "name": "Guest", "code": "guest", "description": "Limited read-only access."},
            
            # Special/System Roles
            {"id": 99, "name": "System API", "code": "system_api", "description": "Role for machine-to-machine (M2M) API integrations."},
        ]
    )


def downgrade() -> None:
    op.execute("DELETE FROM roles WHERE id IN (1, 2, 3, 4, 5, 6, 7, 8, 99)")
