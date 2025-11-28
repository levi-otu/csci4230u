"""Library API endpoints for books and user library management."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_active_user
from src.database import get_db
from src.handlers.library.handler import LibraryHandler
from src.models.user import UserModel
from src.transports.json.library_schemas import (
    AddNotesRequest,
    AddRatingRequest,
    AddReviewRequest,
    BookCreate,
    BookResponse,
    BookUpdate,
    ISBNLookupRequest,
    ISBNLookupResponse,
    LibraryStatsResponse,
    MarkAsReadRequest,
    ReadingListCreate,
    ReadingListItemCreate,
    ReadingListItemResponse,
    ReadingListResponse,
    ReadingListUpdate,
    ReadingListWithItems,
    ReorderItemsRequest,
    UserBookCreate,
    UserBookUpdate,
    UserBookWithDetails,
)

router = APIRouter(prefix="/api/library", tags=["library"])


# Book CRUD Endpoints

@router.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    request: BookCreate,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> BookResponse:
    """Create a new book in the global catalog."""
    handler = LibraryHandler(session)
    return await handler.create_book(request)


@router.get("/books", response_model=List[BookResponse])
async def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> List[BookResponse]:
    """
    Get all books from the catalog.
    Requires authentication.
    """
    handler = LibraryHandler(session)
    return await handler.get_books(skip=skip, limit=limit)


@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> BookResponse:
    """
    Get a specific book by ID.
    Requires authentication.
    """
    handler = LibraryHandler(session)
    return await handler.get_book(book_id)


@router.put("/books/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: UUID,
    request: BookUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> BookResponse:
    """Update a book in the catalog."""
    handler = LibraryHandler(session)
    return await handler.update_book(book_id, request)


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> None:
    """Delete a book from the catalog."""
    handler = LibraryHandler(session)
    await handler.delete_book(book_id)


# ISBN Lookup

@router.post("/books/lookup/isbn", response_model=ISBNLookupResponse)
async def lookup_isbn(
    request: ISBNLookupRequest,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> ISBNLookupResponse:
    """Look up book information by ISBN."""
    handler = LibraryHandler(session)
    return await handler.lookup_isbn(request)


# User Library Endpoints

@router.post("/my-library", response_model=UserBookWithDetails, status_code=status.HTTP_201_CREATED)
async def add_book_to_library(
    request: UserBookCreate,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> UserBookWithDetails:
    """Add a book to user's personal library."""
    handler = LibraryHandler(session)
    return await handler.add_book_to_library(current_user.id, request)


@router.get("/my-library", response_model=List[UserBookWithDetails])
async def get_my_library(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_read: bool | None = Query(None),
    is_favorite: bool | None = Query(None),
    min_rating: float | None = Query(None, ge=0.0, le=5.0),
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> List[UserBookWithDetails]:
    """Get user's personal library with optional filters."""
    handler = LibraryHandler(session)
    return await handler.get_user_library(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        is_read=is_read,
        is_favorite=is_favorite,
        min_rating=min_rating
    )


@router.get("/my-library/{user_book_id}", response_model=UserBookWithDetails)
async def get_library_book(
    user_book_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> UserBookWithDetails:
    """Get a specific book from user's library."""
    handler = LibraryHandler(session)
    return await handler.get_user_book(current_user.id, user_book_id)


@router.put("/my-library/{user_book_id}", response_model=UserBookWithDetails)
async def update_library_book(
    user_book_id: UUID,
    request: UserBookUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> UserBookWithDetails:
    """Update a book in user's library."""
    handler = LibraryHandler(session)
    return await handler.update_user_book(current_user.id, user_book_id, request)


@router.delete("/my-library/{user_book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_library(
    user_book_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> None:
    """Remove a book from user's library."""
    handler = LibraryHandler(session)
    await handler.remove_book_from_library(current_user.id, user_book_id)


# Quick Actions

@router.post("/my-library/{user_book_id}/mark-read", response_model=UserBookWithDetails)
async def mark_as_read(
    user_book_id: UUID,
    request: MarkAsReadRequest,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> UserBookWithDetails:
    """Mark a book as read."""
    handler = LibraryHandler(session)
    return await handler.mark_as_read(current_user.id, user_book_id, request)


@router.post("/my-library/{user_book_id}/mark-unread", response_model=UserBookWithDetails)
async def mark_as_unread(
    user_book_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> UserBookWithDetails:
    """Mark a book as unread."""
    handler = LibraryHandler(session)
    return await handler.mark_as_unread(current_user.id, user_book_id)


@router.post("/my-library/{user_book_id}/reading-status", response_model=UserBookWithDetails)
async def set_reading_status(
    user_book_id: UUID,
    request: dict,  # Expecting {"reading_status": "unread" | "reading" | "finished"}
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> UserBookWithDetails:
    """Set reading status for a book."""
    handler = LibraryHandler(session)
    reading_status = request.get("reading_status")
    if reading_status not in ["unread", "reading", "finished"]:
        raise HTTPException(status_code=400, detail="Invalid reading status")
    return await handler.set_reading_status(current_user.id, user_book_id, reading_status)


@router.post("/my-library/{user_book_id}/rating", response_model=UserBookWithDetails)
async def add_rating(
    user_book_id: UUID,
    request: AddRatingRequest,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> UserBookWithDetails:
    """Add or update rating for a book."""
    handler = LibraryHandler(session)
    return await handler.add_rating(current_user.id, user_book_id, request)


@router.post("/my-library/{user_book_id}/review", response_model=UserBookWithDetails)
async def add_review(
    user_book_id: UUID,
    request: AddReviewRequest,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> UserBookWithDetails:
    """Add or update review for a book."""
    handler = LibraryHandler(session)
    return await handler.add_review(current_user.id, user_book_id, request)


@router.post("/my-library/{user_book_id}/notes", response_model=UserBookWithDetails)
async def add_notes(
    user_book_id: UUID,
    request: AddNotesRequest,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> UserBookWithDetails:
    """Add or update notes for a book."""
    handler = LibraryHandler(session)
    return await handler.add_notes(current_user.id, user_book_id, request)


@router.post("/my-library/{user_book_id}/toggle-favorite", response_model=UserBookWithDetails)
async def toggle_favorite(
    user_book_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> UserBookWithDetails:
    """Toggle favorite status for a book."""
    handler = LibraryHandler(session)
    return await handler.toggle_favorite(current_user.id, user_book_id)


# Reading Lists

@router.post("/reading-lists", response_model=ReadingListResponse, status_code=status.HTTP_201_CREATED)
async def create_reading_list(
    request: ReadingListCreate,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> ReadingListResponse:
    """Create a new reading list."""
    handler = LibraryHandler(session)
    return await handler.create_reading_list(current_user.id, request)


@router.get("/reading-lists", response_model=List[ReadingListResponse])
async def get_reading_lists(
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> List[ReadingListResponse]:
    """Get all reading lists for the current user."""
    handler = LibraryHandler(session)
    return await handler.get_user_reading_lists(current_user.id)


@router.get("/reading-lists/{reading_list_id}", response_model=ReadingListWithItems)
async def get_reading_list(
    reading_list_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> ReadingListWithItems:
    """Get a reading list with all its items."""
    handler = LibraryHandler(session)
    return await handler.get_reading_list(current_user.id, reading_list_id)


@router.put("/reading-lists/{reading_list_id}", response_model=ReadingListResponse)
async def update_reading_list(
    reading_list_id: UUID,
    request: ReadingListUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> ReadingListResponse:
    """Update a reading list."""
    handler = LibraryHandler(session)
    return await handler.update_reading_list(current_user.id, reading_list_id, request)


@router.delete("/reading-lists/{reading_list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reading_list(
    reading_list_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> None:
    """Delete a reading list."""
    handler = LibraryHandler(session)
    await handler.delete_reading_list(current_user.id, reading_list_id)


@router.post(
    "/reading-lists/{reading_list_id}/items",
    response_model=ReadingListItemResponse,
    status_code=status.HTTP_201_CREATED
)
async def add_book_to_reading_list(
    reading_list_id: UUID,
    request: ReadingListItemCreate,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> ReadingListItemResponse:
    """Add a book to a reading list."""
    handler = LibraryHandler(session)
    return await handler.add_book_to_reading_list(
        current_user.id,
        reading_list_id,
        request
    )


@router.delete(
    "/reading-lists/{reading_list_id}/items/{user_book_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def remove_book_from_reading_list(
    reading_list_id: UUID,
    user_book_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> None:
    """Remove a book from a reading list."""
    handler = LibraryHandler(session)
    await handler.remove_book_from_reading_list(
        current_user.id,
        reading_list_id,
        user_book_id
    )


@router.post("/reading-lists/{reading_list_id}/reorder", status_code=status.HTTP_200_OK)
async def reorder_reading_list(
    reading_list_id: UUID,
    request: ReorderItemsRequest,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> bool:
    """Reorder items in a reading list."""
    handler = LibraryHandler(session)
    return await handler.reorder_reading_list(current_user.id, reading_list_id, request)


# Statistics

@router.get("/stats", response_model=LibraryStatsResponse)
async def get_library_stats(
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> LibraryStatsResponse:
    """Get statistics for user's library."""
    handler = LibraryHandler(session)
    return await handler.get_library_stats(current_user.id)
