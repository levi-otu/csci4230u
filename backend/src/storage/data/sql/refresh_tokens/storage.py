"""Storage layer for refresh tokens."""
import hashlib
from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.refresh_token import RefreshTokenModel
from src.storage.data.sql.base_storage import BaseStorage


class RefreshTokenStorage(BaseStorage[RefreshTokenModel]):
    """Storage operations for refresh tokens."""

    def __init__(self, session: AsyncSession):
        """
        Initialize refresh token storage.

        Args:
            session: Database session.
        """
        super().__init__(RefreshTokenModel, session)

    @staticmethod
    def hash_token(token: str) -> str:
        """
        Hash a token for secure storage.

        Args:
            token: The token to hash.

        Returns:
            str: The hashed token.
        """
        return hashlib.sha256(token.encode()).hexdigest()

    async def create_token(
        self,
        user_id: UUID,
        token: str,
        expires_at: datetime,
        device_info: str | None = None,
        ip_address: str | None = None
    ) -> RefreshTokenModel:
        """
        Create a new refresh token.

        Args:
            user_id: The user ID.
            token: The refresh token (will be hashed).
            expires_at: Token expiration time.
            device_info: Optional device information.
            ip_address: Optional IP address.

        Returns:
            RefreshTokenModel: The created token.
        """
        token_hash = self.hash_token(token)

        refresh_token = RefreshTokenModel(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            device_info=device_info,
            ip_address=ip_address
        )

        self.session.add(refresh_token)
        await self.session.flush()
        await self.session.refresh(refresh_token)

        return refresh_token

    async def get_by_token(self, token: str) -> RefreshTokenModel | None:
        """
        Get refresh token by token value.

        Args:
            token: The token to look up.

        Returns:
            RefreshTokenModel | None: The token if found.
        """
        token_hash = self.hash_token(token)
        stmt = select(RefreshTokenModel).where(RefreshTokenModel.token_hash == token_hash)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_token_hash(self, token_hash: str) -> RefreshTokenModel | None:
        """
        Get refresh token by hash.

        Args:
            token_hash: The token hash to look up.

        Returns:
            RefreshTokenModel | None: The token if found.
        """
        stmt = select(RefreshTokenModel).where(RefreshTokenModel.token_hash == token_hash)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def revoke_token(self, token_id: UUID, replaced_by: UUID | None = None) -> bool:
        """
        Revoke a refresh token.

        Args:
            token_id: The token ID to revoke.
            replaced_by: Optional ID of replacement token (for rotation).

        Returns:
            bool: True if token was revoked.
        """
        stmt = (
            update(RefreshTokenModel)
            .where(RefreshTokenModel.id == token_id)
            .values(revoked=True, replaced_by_token_id=replaced_by)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount > 0

    async def revoke_all_user_tokens(self, user_id: UUID) -> int:
        """
        Revoke all tokens for a user (logout all devices).

        Args:
            user_id: The user ID.

        Returns:
            int: Number of tokens revoked.
        """
        stmt = (
            update(RefreshTokenModel)
            .where(RefreshTokenModel.user_id == user_id)
            .where(RefreshTokenModel.revoked == False)  # noqa: E712
            .values(revoked=True)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

    async def cleanup_expired_tokens(self) -> int:
        """
        Delete expired and revoked tokens (background job).

        Returns:
            int: Number of tokens deleted.
        """
        now = datetime.now(datetime.now().astimezone().tzinfo)

        # Delete tokens that are either:
        # 1. Expired by more than 7 days
        # 2. Revoked and older than 30 days
        stmt = delete(RefreshTokenModel).where(
            (RefreshTokenModel.expires_at < now) |
            ((RefreshTokenModel.revoked == True) & (RefreshTokenModel.created_at < now))  # noqa: E712
        )

        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

    async def get_user_tokens(self, user_id: UUID) -> list[RefreshTokenModel]:
        """
        Get all active tokens for a user.

        Args:
            user_id: The user ID.

        Returns:
            list[RefreshTokenModel]: List of active tokens.
        """
        stmt = (
            select(RefreshTokenModel)
            .where(RefreshTokenModel.user_id == user_id)
            .where(RefreshTokenModel.revoked == False)  # noqa: E712
            .order_by(RefreshTokenModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
