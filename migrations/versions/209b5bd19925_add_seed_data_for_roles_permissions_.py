"""Add seed data for roles, permissions, role-permissions and users

Revision ID: 209b5bd19925
Revises: 1f16b6937b04
Create Date: 2025-03-19 08:16:38.638732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '209b5bd19925'
down_revision: Union[str, None] = '1f16b6937b04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        INSERT INTO roles (id, name, created_at, created_by) VALUES
            (1, 'Super User', NOW(), 'system'),
            (2, 'User', NOW(), 'system');

        INSERT INTO permissions (id, name, created_at, created_by) VALUES
            (1, 'Can create user', NOW(), 'system'),
            (2, 'Can view users', NOW(), 'system'),
            (3, 'Can update user', NOW(), 'system'),
            (4, 'Can deactivate user', NOW(), 'system'),
            (5, 'Can activate user', NOW(), 'system'),
            (6, 'Can delete user', NOW(), 'system'),
            (7, 'Can create role', NOW(), 'system'),
            (8, 'Can view roles', NOW(), 'system'),
            (9, 'Can update role', NOW(), 'system'),
            (10, 'Can delete role', NOW(), 'system');

        INSERT INTO role_permissions (role_id, permission_id, created_at, created_by) VALUES
            (1, 1, NOW(), 'system'), 
            (1, 2, NOW(), 'system'), 
            (1, 3, NOW(), 'system'), 
            (1, 4, NOW(), 'system'), 
            (1, 5, NOW(), 'system'), 
            (1, 6, NOW(), 'system'),
            (1, 7, NOW(), 'system'), 
            (1, 8, NOW(), 'system'), 
            (1, 9, NOW(), 'system'), 
            (1, 10, NOW(), 'system'),
            (2, 1, NOW(), 'system'), 
            (2, 2, NOW(), 'system');

        INSERT INTO users (username, email, hashed_password, role_id, status_id, is_active, created_at, created_by) VALUES
            ('superuser', 'admin@example.com', 
            '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 
            1, 1, true, NOW(), 'system');
    """)

def downgrade():
    op.execute("DELETE FROM users WHERE email = 'admin@example.com';")
    op.execute("DELETE FROM role_permissions;")
    op.execute("DELETE FROM permissions;")
    op.execute("DELETE FROM roles;")
