"""Add roles table and seed admin user

Revision ID: 379a81d365b7
Revises: 379a81d365b6
Create Date: 2025-11-20 19:00:00.000000

"""
import uuid
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext

# revision identifiers, used by Alembic.
revision: str = '379a81d365b7'
down_revision: Union[str, Sequence[str], None] = '379a81d365b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def upgrade() -> None:
    """Add roles tables and seed admin user."""
    # Create roles table
    op.create_table(
        'roles',
        sa.Column('id', sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_id'), 'roles', ['id'], unique=False)
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)

    # Create user_roles association table
    op.create_table(
        'user_roles',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('role_id', sa.UUID(), nullable=False),
        sa.Column('assigned_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )

    # Create groups table
    op.create_table(
        'groups',
        sa.Column('id', sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('created_by', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_groups_id'), 'groups', ['id'], unique=False)
    op.create_index(op.f('ix_groups_name'), 'groups', ['name'], unique=False)

    # Create user_groups association table
    op.create_table(
        'user_groups',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('group_id', sa.UUID(), nullable=False),
        sa.Column('joined_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id']),
        sa.PrimaryKeyConstraint('user_id', 'group_id')
    )

    # Seed data using raw SQL with f-strings (UUIDs are safe)
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    admin_user_id = str(uuid.uuid4())
    admin_role_id = str(uuid.uuid4())
    admin_security_id = str(uuid.uuid4())

    # Hash password
    hashed_password = pwd_context.hash("Admin@12345")
    # Escape single quotes in password hash
    hashed_password_escaped = hashed_password.replace("'", "''")

    # Insert admin role
    op.execute(
        f"""
        INSERT INTO roles (id, name, description, created_at, updated_at)
        VALUES ('{admin_role_id}'::uuid, 'admin', 'Administrator with full access', '{now_str}', '{now_str}')
        """
    )

    # Insert admin user
    op.execute(
        f"""
        INSERT INTO users (id, username, email, full_name, is_active, created_at, updated_at)
        VALUES ('{admin_user_id}'::uuid, 'admin', 'test@example.com', 'Super Admin', true, '{now_str}', '{now_str}')
        """
    )

    # Insert admin user security
    op.execute(
        f"""
        INSERT INTO user_security (id, user_id, email, password, password_changed_at, created_at, updated_at)
        VALUES ('{admin_security_id}'::uuid, '{admin_user_id}'::uuid, 'test@example.com', '{hashed_password_escaped}', '{now_str}', '{now_str}', '{now_str}')
        """
    )

    # Assign admin role to admin user
    op.execute(
        f"""
        INSERT INTO user_roles (user_id, role_id, assigned_at)
        VALUES ('{admin_user_id}'::uuid, '{admin_role_id}'::uuid, '{now_str}')
        """
    )


def downgrade() -> None:
    """Remove roles tables and seed data."""
    # Remove seed data
    op.execute(sa.text("DELETE FROM user_roles"))
    op.execute(sa.text("DELETE FROM user_security WHERE email = 'test@example.com'"))
    op.execute(sa.text("DELETE FROM users WHERE username = 'admin'"))
    op.execute(sa.text("DELETE FROM roles WHERE name = 'admin'"))

    # Drop tables
    op.drop_table('user_groups')
    op.drop_index(op.f('ix_groups_name'), table_name='groups')
    op.drop_index(op.f('ix_groups_id'), table_name='groups')
    op.drop_table('groups')
    op.drop_table('user_roles')
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_index(op.f('ix_roles_id'), table_name='roles')
    op.drop_table('roles')
