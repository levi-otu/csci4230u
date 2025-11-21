"""Base storage with generic CRUD operations."""
from typing import Any, Generic, List, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseStorage(Generic[ModelType]):
    """Generic storage for CRUD operations."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        """
        Initialize storage.

        Args:
            model: The SQLAlchemy model class.
            session: The database session.
        """
        self.model = model
        self.session = session

    async def create(self, **kwargs: Any) -> ModelType:
        """
        Create a new record.

        Args:
            **kwargs: Fields for the new record.

        Returns:
            ModelType: The created record.
        """
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, id: UUID) -> Optional[ModelType]:
        """
        Get a record by ID.

        Args:
            id: The record ID.

        Returns:
            Optional[ModelType]: The record if found, None otherwise.
        """
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        Get all records with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[ModelType]: List of records.
        """
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(
        self,
        id: UUID,
        **kwargs: Any
    ) -> Optional[ModelType]:
        """
        Update a record.

        Args:
            id: The record ID.
            **kwargs: Fields to update.

        Returns:
            Optional[ModelType]: The updated record if found, None otherwise.
        """
        instance = await self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            await self.session.flush()
            await self.session.refresh(instance)
        return instance

    async def delete(self, id: UUID) -> bool:
        """
        Delete a record.

        Args:
            id: The record ID.

        Returns:
            bool: True if deleted, False if not found.
        """
        instance = await self.get_by_id(id)
        if instance:
            await self.session.delete(instance)
            await self.session.flush()
            return True
        return False
