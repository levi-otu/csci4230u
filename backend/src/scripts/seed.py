"""Seed script to create initial admin user."""
import asyncio
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import AsyncSessionLocal
from src.models.user import User, UserSecurity
from src.models.role import Role
from src.security import get_password_hash


async def seed_admin_user() -> None:
    """Create initial admin user if not exists."""
    async with AsyncSessionLocal() as session:
        # Check if admin user already exists
        stmt = select(User).where(User.username == "admin")
        result = await session.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print("Admin user already exists. Skipping seed.")
            return

        # Create admin role if not exists
        role_stmt = select(Role).where(Role.name == "admin")
        role_result = await session.execute(role_stmt)
        admin_role = role_result.scalar_one_or_none()

        if not admin_role:
            admin_role = Role(
                name="admin",
                description="Administrator with full access"
            )
            session.add(admin_role)
            await session.flush()
            print("Created admin role.")

        # Create admin user
        admin_user = User(
            username="admin",
            email="test@example.com",
            full_name="Super Admin",
            is_active=True
        )
        session.add(admin_user)
        await session.flush()

        # Create user security with hashed password
        admin_security = UserSecurity(
            user_id=admin_user.id,
            email="test@example.com",
            password=get_password_hash("Admin@12345"),
            password_changed_at=datetime.utcnow()
        )
        session.add(admin_security)

        # Assign admin role to user
        admin_user.roles.append(admin_role)

        await session.commit()
        print(f"Created admin user:")
        print(f"  Username: admin")
        print(f"  Email: test@example.com")
        print(f"  Password: Admin@12345")


if __name__ == "__main__":
    asyncio.run(seed_admin_user())
