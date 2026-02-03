"""seed_role_permissions_data

Revision ID: fb1c5dc81128
Revises: c63f7fc627a9
Create Date: 2026-02-02 14:52:20.555079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb1c5dc81128'
down_revision: Union[str, None] = 'c63f7fc627a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy.sql import table, column
from sqlalchemy import Integer

def upgrade() -> None:
    # Definisi tabel sementara untuk operasi bulk_insert
    role_permissions_table = table('role_permissions',
        column('role_id', Integer),
        column('permission_id', Integer)
    )

    op.bulk_insert(role_permissions_table,
        [
            # --- 1. Super Administrator (Role: 1) ---
            # All Permissions
            {"role_id": 1, "permission_id": 1}, {"role_id": 1, "permission_id": 2}, {"role_id": 1, "permission_id": 3},
            {"role_id": 1, "permission_id": 4}, {"role_id": 1, "permission_id": 5}, {"role_id": 1, "permission_id": 6},
            {"role_id": 1, "permission_id": 7}, {"role_id": 1, "permission_id": 8}, {"role_id": 1, "permission_id": 9},
            {"role_id": 1, "permission_id": 10}, {"role_id": 1, "permission_id": 11}, {"role_id": 1, "permission_id": 12},
            {"role_id": 1, "permission_id": 13}, {"role_id": 1, "permission_id": 14}, {"role_id": 1, "permission_id": 15},
            {"role_id": 1, "permission_id": 16}, {"role_id": 1, "permission_id": 17},
            {"role_id": 1, "permission_id": 18}, {"role_id": 1, "permission_id": 19}, {"role_id": 1, "permission_id": 20},

            # --- 2. Administrator (Role: 2) ---
            # Full User & Role Management, Dashboard, Settings. No Permission Management.
            {"role_id": 2, "permission_id": 1}, {"role_id": 2, "permission_id": 2}, {"role_id": 2, "permission_id": 3},
            {"role_id": 2, "permission_id": 4}, {"role_id": 2, "permission_id": 5}, # User CRUD + List
            {"role_id": 2, "permission_id": 6}, {"role_id": 2, "permission_id": 7}, {"role_id": 2, "permission_id": 8},
            {"role_id": 2, "permission_id": 9}, {"role_id": 2, "permission_id": 10}, # Role CRUD + List
            {"role_id": 2, "permission_id": 12}, {"role_id": 2, "permission_id": 15}, # View Perms only
            {"role_id": 2, "permission_id": 16}, {"role_id": 2, "permission_id": 17}, # Dashboard, Settings
            {"role_id": 2, "permission_id": 19}, # View Assigned Perms

            # --- 3. Manager (Role: 3) ---
            # View Only for User/Role, Access Dashboard
            {"role_id": 3, "permission_id": 2}, {"role_id": 3, "permission_id": 5}, # View User
            {"role_id": 3, "permission_id": 7}, {"role_id": 3, "permission_id": 10}, # View Role
            {"role_id": 3, "permission_id": 16}, # Dashboard

            # --- 4. Editor (Role: 4) ---
            # Dashboard Access
            {"role_id": 4, "permission_id": 16},

            # --- 5. Moderator (Role: 5) ---
            # View User List + Dashboard (to moderate)
            {"role_id": 5, "permission_id": 5}, {"role_id": 5, "permission_id": 16},

            # --- 6. Support (Role: 6) ---
            # View User Details & List, Dashboard
            {"role_id": 6, "permission_id": 2}, {"role_id": 6, "permission_id": 5}, {"role_id": 6, "permission_id": 16},

            # --- 7. Standard User (Role: 7) ---
            # No System Permissions (Own profile handled by logic, not global permission)
            
            # --- 8. Guest (Role: 8) ---
            # No Permissions
            
            # --- 99. System API (Role: 99) ---
            # Full User Management (for sync)
            {"role_id": 99, "permission_id": 1}, {"role_id": 99, "permission_id": 2},
            {"role_id": 99, "permission_id": 3}, {"role_id": 99, "permission_id": 4}, 
            {"role_id": 99, "permission_id": 5},
        ]
    )


def downgrade() -> None:
    # Hapus semua mapping untuk role yang di-seed
    op.execute("DELETE FROM role_permissions WHERE role_id IN (1, 2, 3, 4, 5, 6, 7, 8, 99)")
