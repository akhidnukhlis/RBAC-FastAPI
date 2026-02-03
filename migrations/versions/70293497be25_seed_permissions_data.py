"""seed_permissions_data

Revision ID: 70293497be25
Revises: ab334ca26fda
Create Date: 2026-02-02 14:39:55.966150

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70293497be25'
down_revision: Union[str, None] = 'ab334ca26fda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

def upgrade() -> None:
    # Definisi tabel sementara untuk operasi bulk_insert
    permissions_table = table('permissions',
        column('id', Integer),
        column('name', String),
        column('code', String),
        column('description', String)
    )

    op.bulk_insert(permissions_table,
        [
            # User Management
            {"id": 1, "name": "Create User", "code": "user:create", "description": "Can create new users"},
            {"id": 2, "name": "View User", "code": "user:read", "description": "Can view user details"},
            {"id": 3, "name": "Update User", "code": "user:update", "description": "Can update user details"},
            {"id": 4, "name": "Delete User", "code": "user:delete", "description": "Can delete users"},
            {"id": 5, "name": "View User List", "code": "user:list", "description": "Can view list of users"},

            # Role Management
            {"id": 6, "name": "Create Role", "code": "role:create", "description": "Can create new roles"},
            {"id": 7, "name": "View Role", "code": "role:read", "description": "Can view role details"},
            {"id": 8, "name": "Update Role", "code": "role:update", "description": "Can update role details"},
            {"id": 9, "name": "Delete Role", "code": "role:delete", "description": "Can delete roles"},
            {"id": 10, "name": "View Role List", "code": "role:list", "description": "Can view list of roles"},

            # Permission Management
            {"id": 11, "name": "Create Permission", "code": "permission:create", "description": "Can create new permissions"},
            {"id": 12, "name": "View Permission", "code": "permission:read", "description": "Can view permission details"},
            {"id": 13, "name": "Update Permission", "code": "permission:update", "description": "Can update permission details"},
            {"id": 14, "name": "Delete Permission", "code": "permission:delete", "description": "Can delete permissions"},
            {"id": 15, "name": "View Permission List", "code": "permission:list", "description": "Can view list of permissions"},
            
            # Application/System Access
            {"id": 16, "name": "Access Dashboard", "code": "system:dashboard", "description": "Can access admin dashboard"},
            {"id": 17, "name": "Manage Settings", "code": "system:settings", "description": "Can manage system settings"},

            # Role Permissions Management (Assigning permissions to roles)
            {"id": 18, "name": "Assign Permissions", "code": "role_permission:create", "description": "Can assign permissions to roles"},
            {"id": 19, "name": "View Assigned Permissions", "code": "role_permission:read", "description": "Can view permissions assigned to roles"},
            {"id": 20, "name": "Revoke Permissions", "code": "role_permission:delete", "description": "Can revoke permissions from roles"},
        ]
    )


def downgrade() -> None:
    op.execute("DELETE FROM permissions WHERE id BETWEEN 1 AND 20")
