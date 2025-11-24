"""Library handler for book and reading list business logic."""
from datetime import datetime
from typing import List
from uuid import UUID

import httpx
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.book import BookModel, UserBookModel, ReadingListModel
from src.models.user import UserModel
from src.storage.data.sql.books.storage import BookStorage
from src.storage.data.sql.user.books.storage import UserBookStorage, ReadingListStorage
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
    UserBookResponse,
    UserBookUpdate,
    UserBookWithDetails,
)


class LibraryHandler:
    """Handler for library operations."""

    def __init__(self, session: AsyncSession):
        """
        Initialize library handler.

        Args:
            session: Database session.
        """
        self.session = session
        self.book_repo = BookStorage(session)
        self.user_book_repo = UserBookStorage(session)
        self.reading_list_repo = ReadingListStorage(session)

    async def _user_book_to_details(self, user_book: UserBookModel) -> UserBookWithDetails:
        """
        Convert a UserBookModel to UserBookWithDetails by fetching the related book.

        Args:
            user_book: The user book model.

        Returns:
            UserBookWithDetails with the book populated.
        """
        book = await self.book_repo.get_by_id(user_book.book_id)
        user_book_dict = {
            'id': user_book.id,
            'user_id': user_book.user_id,
            'book_id': user_book.book_id,
            'book_version_id': user_book.book_version_id,
            'added_date': user_book.added_date,
            'is_read': user_book.is_read,
            'read_date': user_book.read_date,
            'reading_status': user_book.reading_status,
            'rating': user_book.rating,
            'review': user_book.review,
            'notes': user_book.notes,
            'is_favorite': user_book.is_favorite,
            'book': BookResponse.model_validate(book) if book else None
        }
        return UserBookWithDetails.model_validate(user_book_dict)

    # Book CRUD Operations

    async def create_book(self, request: BookCreate) -> BookResponse:
        """
        Create a new book.

        Args:
            request: Book creation data.

        Returns:
            BookResponse: The created book.
        """
        try:
            book = await self.book_repo.create(**request.model_dump())
            return BookResponse.model_validate(book)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create book: {str(e)}"
            )

    async def get_book(self, book_id: UUID) -> BookResponse:
        """Get a book by ID."""
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return BookResponse.model_validate(book)

    async def get_books(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[BookResponse]:
        """Get all books with pagination."""
        books = await self.book_repo.get_all(skip=skip, limit=limit)
        return [BookResponse.model_validate(book) for book in books]

    async def update_book(
        self,
        book_id: UUID,
        request: BookUpdate
    ) -> BookResponse:
        """Update a book."""
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )

        update_data = request.model_dump(exclude_unset=True)
        updated_book = await self.book_repo.update(book_id, **update_data)
        if not updated_book:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update book"
            )
        return BookResponse.model_validate(updated_book)

    async def delete_book(self, book_id: UUID) -> bool:
        """Delete a book."""
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return await self.book_repo.delete(book_id)

    # ISBN Lookup

    async def lookup_isbn(self, request: ISBNLookupRequest) -> ISBNLookupResponse:
        """
        Look up book information by ISBN using Open Library API.

        Args:
            request: ISBN lookup request.

        Returns:
            ISBNLookupResponse: Book information from external API.
        """
        isbn = request.isbn
        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                data = response.json()

                # Log the full response for debugging
                import json
                print("=" * 80)
                print(f"Open Library API Response for ISBN {isbn}:")
                print(json.dumps(data, indent=2))
                print("=" * 80)

                # Check if book was found
                book_key = f"ISBN:{isbn}"
                if book_key not in data:
                    return ISBNLookupResponse(found=False)

                book_data = data[book_key]
                print(f"Extracted book_data:")
                print(json.dumps(book_data, indent=2))
                print("=" * 80)

                # Extract book information
                authors = book_data.get("authors", [])
                author_names = ", ".join([a.get("name", "") for a in authors])

                # Extract publishers - join multiple if present
                publishers = book_data.get("publishers", [])
                publisher_names = ", ".join([p.get("name", "") for p in publishers if p.get("name")])
                publisher_name = publisher_names if publisher_names else None

                # Try to get cover image - Open Library provides covers via a different endpoint
                # We can construct the cover URL from the book key if available
                cover_url = None
                if "cover" in book_data:
                    cover = book_data["cover"]
                    cover_url = cover.get("large") or cover.get("medium") or cover.get("small")
                # If no cover in data, we could construct from Open Library Cover API
                # Format: https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg
                if not cover_url and isbn:
                    cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

                # Extract genre from subjects - take first relevant subject
                subjects = book_data.get("subjects", [])
                genre = None
                if subjects:
                    # Try to find a good genre from subjects
                    genre_keywords = ["fiction", "literature", "mystery", "romance", "science fiction",
                                     "fantasy", "thriller", "horror", "biography", "history"]
                    for subject in subjects:
                        subject_name = subject.get("name", "").lower()
                        for keyword in genre_keywords:
                            if keyword in subject_name:
                                genre = subject.get("name")
                                break
                        if genre:
                            break
                    # If no genre keyword found, just use first subject
                    if not genre and subjects:
                        genre = subjects[0].get("name")

                # Get description from notes or subtitle
                description = book_data.get("notes") or book_data.get("subtitle")

                # Detect multi-volume series
                series_title = None
                volume_number = None
                volume_title = None
                total_volumes = None

                # Check table of contents for volume information
                toc = book_data.get("table_of_contents", [])
                if toc and len(toc) > 1:
                    # Check if TOC entries look like volume listings (e.g., "v. 1. Title")
                    import re
                    volume_pattern = re.compile(r'^v\.?\s*(\d+)\.?\s*(.+)$', re.IGNORECASE)

                    # Count how many TOC entries match the volume pattern
                    volume_matches = []
                    for entry in toc:
                        entry_title = entry.get("title", "")
                        match = volume_pattern.match(entry_title.strip())
                        if match:
                            volume_matches.append({
                                "number": int(match.group(1)),
                                "title": match.group(2).strip()
                            })

                    # If we have multiple volume entries, this is a multi-volume work
                    if len(volume_matches) > 1:
                        total_volumes = len(volume_matches)
                        series_title = book_data.get("title")  # The main title is the series title

                        # Try to determine which volume this ISBN represents
                        # We'll look at which ISBNs are present and try to match position
                        identifiers = book_data.get("identifiers", {})
                        isbn_list = identifiers.get("isbn_13", []) or identifiers.get("isbn_10", [])

                        # If the number of ISBNs matches the number of volumes, assume they're in order
                        if len(isbn_list) == total_volumes:
                            # Find which position our ISBN is in the list
                            for i, book_isbn in enumerate(isbn_list):
                                if book_isbn == isbn or book_isbn.replace("-", "") == isbn.replace("-", ""):
                                    volume_number = i + 1
                                    if volume_number <= len(volume_matches):
                                        volume_title = volume_matches[volume_number - 1]["title"]
                                    break

                        # If we couldn't determine the volume, default to volume 1
                        if volume_number is None and volume_matches:
                            volume_number = 1
                            volume_title = volume_matches[0]["title"]

                return ISBNLookupResponse(
                    found=True,
                    title=book_data.get("title"),
                    author=author_names or None,
                    publisher=publisher_name,
                    publish_date=book_data.get("publish_date"),
                    genre=genre,
                    isbn_10=book_data.get("identifiers", {}).get("isbn_10", [None])[0],
                    isbn_13=book_data.get("identifiers", {}).get("isbn_13", [None])[0],
                    cover_url=cover_url,
                    description=description,
                    page_count=book_data.get("number_of_pages"),
                    series_title=series_title,
                    volume_number=volume_number,
                    volume_title=volume_title,
                    total_volumes=total_volumes
                )

        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to lookup ISBN: {str(e)}"
            )

    # User Library Operations

    async def add_book_to_library(
        self,
        user_id: UUID,
        request: UserBookCreate
    ) -> UserBookResponse:
        """
        Add a book to user's library.

        Args:
            user_id: The user's ID.
            request: User book creation data.

        Returns:
            UserBookResponse: The created user book.
        """
        # Verify book exists
        book = await self.book_repo.get_by_id(request.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )

        # Check if book already in library
        existing = await self.user_book_repo.get_user_book(user_id, request.book_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book already in library"
            )

        try:
            user_book = await self.user_book_repo.create(
                user_id=user_id,
                **request.model_dump()
            )
            response = UserBookResponse.model_validate(user_book)
            response.book = BookResponse.model_validate(book)
            return response
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to add book to library: {str(e)}"
            )

    async def get_user_library(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        is_read: bool | None = None,
        is_favorite: bool | None = None,
        min_rating: float | None = None
    ) -> List[UserBookWithDetails]:
        """Get user's library with filters."""
        user_books = await self.user_book_repo.get_user_library(
            user_id=user_id,
            skip=skip,
            limit=limit,
            is_read=is_read,
            is_favorite=is_favorite,
            min_rating=min_rating
        )

        results = []
        for user_book in user_books:
            response = await self._user_book_to_details(user_book)
            results.append(response)

        return results

    async def get_user_book(
        self,
        user_id: UUID,
        user_book_id: UUID
    ) -> UserBookWithDetails:
        """Get a specific book from user's library."""
        user_book = await self.user_book_repo.get_by_id(user_book_id)
        if not user_book or user_book.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found in your library"
            )

        return await self._user_book_to_details(user_book)

    async def update_user_book(
        self,
        user_id: UUID,
        user_book_id: UUID,
        request: UserBookUpdate
    ) -> UserBookWithDetails:
        """Update a book in user's library."""
        user_book = await self.user_book_repo.get_by_id(user_book_id)
        if not user_book or user_book.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found in your library"
            )

        update_data = request.model_dump(exclude_unset=True)
        updated_user_book = await self.user_book_repo.update(user_book_id, **update_data)
        if not updated_user_book:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update book"
            )

        return await self._user_book_to_details(updated_user_book)

    async def remove_book_from_library(
        self,
        user_id: UUID,
        user_book_id: UUID
    ) -> bool:
        """Remove a book from user's library."""
        user_book = await self.user_book_repo.get_by_id(user_book_id)
        if not user_book or user_book.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found in your library"
            )

        return await self.user_book_repo.delete(user_book_id)

    async def mark_as_read(
        self,
        user_id: UUID,
        user_book_id: UUID,
        request: MarkAsReadRequest
    ) -> UserBookWithDetails:
        """Mark a book as read."""
        user_book = await self.user_book_repo.get_by_id(user_book_id)
        if not user_book or user_book.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found in your library"
            )

        # Use provided read_date or default to now
        read_date = request.read_date if request.read_date else datetime.now()
        updated = await self.user_book_repo.mark_as_read(user_book_id, read_date)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to mark book as read"
            )

        return await self._user_book_to_details(updated)

    async def mark_as_unread(
        self,
        user_id: UUID,
        user_book_id: UUID
    ) -> UserBookWithDetails:
        """Mark a book as unread."""
        user_book = await self.user_book_repo.get_by_id(user_book_id)
        if not user_book or user_book.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found in your library"
            )

        updated = await self.user_book_repo.mark_as_unread(user_book_id)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to mark book as unread"
            )

        return await self._user_book_to_details(updated)

    async def set_reading_status(
        self,
        user_id: UUID,
        user_book_id: UUID,
        reading_status: str
    ) -> UserBookWithDetails:
        """Set reading status for a book."""
        user_book = await self.user_book_repo.get_by_id(user_book_id)
        if not user_book or user_book.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found in your library"
            )

        updated = await self.user_book_repo.set_reading_status(user_book_id, reading_status)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update reading status"
            )

        return await self._user_book_to_details(updated)

    async def add_rating(
        self,
        user_id: UUID,
        user_book_id: UUID,
        request: AddRatingRequest
    ) -> UserBookWithDetails:
        """Add or update rating."""
        user_book = await self.user_book_repo.get_by_id(user_book_id)
        if not user_book or user_book.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found in your library"
            )

        updated = await self.user_book_repo.add_rating(user_book_id, request.rating)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add rating"
            )

        book = await self.book_repo.get_by_id(updated.book_id)
        response = await self._user_book_to_details(updated)
        if book:
            response.book = BookResponse.model_validate(book)
        return response

    async def add_review(
        self,
        user_id: UUID,
        user_book_id: UUID,
        request: AddReviewRequest
    ) -> UserBookWithDetails:
        """Add or update review."""
        user_book = await self.user_book_repo.get_by_id(user_book_id)
        if not user_book or user_book.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found in your library"
            )

        updated = await self.user_book_repo.add_review(user_book_id, request.review)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add review"
            )

        book = await self.book_repo.get_by_id(updated.book_id)
        response = await self._user_book_to_details(updated)
        if book:
            response.book = BookResponse.model_validate(book)
        return response

    async def add_notes(
        self,
        user_id: UUID,
        user_book_id: UUID,
        request: AddNotesRequest
    ) -> UserBookWithDetails:
        """Add or update notes."""
        user_book = await self.user_book_repo.get_by_id(user_book_id)
        if not user_book or user_book.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found in your library"
            )

        updated = await self.user_book_repo.add_notes(user_book_id, request.notes)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add notes"
            )

        book = await self.book_repo.get_by_id(updated.book_id)
        response = await self._user_book_to_details(updated)
        if book:
            response.book = BookResponse.model_validate(book)
        return response

    async def toggle_favorite(
        self,
        user_id: UUID,
        user_book_id: UUID
    ) -> UserBookWithDetails:
        """Toggle favorite status."""
        user_book = await self.user_book_repo.get_by_id(user_book_id)
        if not user_book or user_book.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found in your library"
            )

        updated = await self.user_book_repo.toggle_favorite(user_book_id)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to toggle favorite"
            )

        book = await self.book_repo.get_by_id(updated.book_id)
        response = await self._user_book_to_details(updated)
        if book:
            response.book = BookResponse.model_validate(book)
        return response

    # Reading List Operations

    async def create_reading_list(
        self,
        user_id: UUID,
        request: ReadingListCreate
    ) -> ReadingListResponse:
        """Create a new reading list."""
        try:
            reading_list = await self.reading_list_repo.create(
                user_id=user_id,
                name=request.name,
                description=request.description,
                is_default=request.is_default
            )
            response = ReadingListResponse.model_validate(reading_list)
            response.item_count = 0
            return response
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create reading list: {str(e)}"
            )

    async def get_user_reading_lists(self, user_id: UUID) -> List[ReadingListResponse]:
        """Get all reading lists for a user."""
        lists = await self.reading_list_repo.get_user_reading_lists(user_id)
        results = []
        for reading_list in lists:
            response = ReadingListResponse.model_validate(reading_list)
            items = await self.reading_list_repo.get_list_items(reading_list.id)
            response.item_count = len(items)
            results.append(response)
        return results

    async def get_reading_list(
        self,
        user_id: UUID,
        reading_list_id: UUID
    ) -> ReadingListWithItems:
        """Get a reading list with items."""
        reading_list = await self.reading_list_repo.get_by_id(reading_list_id)
        if not reading_list or reading_list.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reading list not found"
            )

        items = await self.reading_list_repo.get_list_items(reading_list_id)
        item_responses = []
        for item in items:
            user_book = await self.user_book_repo.get_by_id(item.user_book_id)
            if user_book:
                book = await self.book_repo.get_by_id(user_book.book_id)
                user_book_response = UserBookWithDetails.model_validate(user_book)
                if book:
                    user_book_response.book = BookResponse.model_validate(book)

                item_response = ReadingListItemResponse.model_validate(item)
                item_response.user_book = user_book_response
                item_responses.append(item_response)

        response = ReadingListWithItems.model_validate(reading_list)
        response.items = item_responses
        response.item_count = len(item_responses)
        return response

    async def update_reading_list(
        self,
        user_id: UUID,
        reading_list_id: UUID,
        request: ReadingListUpdate
    ) -> ReadingListResponse:
        """Update a reading list."""
        reading_list = await self.reading_list_repo.get_by_id(reading_list_id)
        if not reading_list or reading_list.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reading list not found"
            )

        update_data = request.model_dump(exclude_unset=True)
        updated = await self.reading_list_repo.update(reading_list_id, **update_data)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update reading list"
            )

        response = ReadingListResponse.model_validate(updated)
        items = await self.reading_list_repo.get_list_items(reading_list_id)
        response.item_count = len(items)
        return response

    async def delete_reading_list(
        self,
        user_id: UUID,
        reading_list_id: UUID
    ) -> bool:
        """Delete a reading list."""
        reading_list = await self.reading_list_repo.get_by_id(reading_list_id)
        if not reading_list or reading_list.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reading list not found"
            )

        return await self.reading_list_repo.delete(reading_list_id)

    async def add_book_to_reading_list(
        self,
        user_id: UUID,
        reading_list_id: UUID,
        request: ReadingListItemCreate
    ) -> ReadingListItemResponse:
        """Add a book to a reading list."""
        reading_list = await self.reading_list_repo.get_by_id(reading_list_id)
        if not reading_list or reading_list.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reading list not found"
            )

        user_book = await self.user_book_repo.get_by_id(request.user_book_id)
        if not user_book or user_book.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found in your library"
            )

        try:
            item = await self.reading_list_repo.add_book_to_list(
                reading_list_id,
                request.user_book_id,
                request.order_index
            )
            return ReadingListItemResponse.model_validate(item)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to add book to reading list: {str(e)}"
            )

    async def remove_book_from_reading_list(
        self,
        user_id: UUID,
        reading_list_id: UUID,
        user_book_id: UUID
    ) -> bool:
        """Remove a book from a reading list."""
        reading_list = await self.reading_list_repo.get_by_id(reading_list_id)
        if not reading_list or reading_list.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reading list not found"
            )

        return await self.reading_list_repo.remove_book_from_list(
            reading_list_id,
            user_book_id
        )

    async def reorder_reading_list(
        self,
        user_id: UUID,
        reading_list_id: UUID,
        request: ReorderItemsRequest
    ) -> bool:
        """Reorder items in a reading list."""
        reading_list = await self.reading_list_repo.get_by_id(reading_list_id)
        if not reading_list or reading_list.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reading list not found"
            )

        return await self.reading_list_repo.reorder_items(request.items)

    # Statistics

    async def get_library_stats(self, user_id: UUID) -> LibraryStatsResponse:
        """Get library statistics for a user."""
        all_books = await self.user_book_repo.get_user_library(user_id, limit=10000)

        total_books = len(all_books)
        read_books = sum(1 for book in all_books if book.is_read)
        favorite_books = sum(1 for book in all_books if book.is_favorite)

        # Calculate average rating
        rated_books = [book for book in all_books if book.rating is not None]
        average_rating = (
            sum(book.rating for book in rated_books) / len(rated_books)
            if rated_books else None
        )

        # Get reading lists count
        reading_lists = await self.reading_list_repo.get_user_reading_lists(user_id)

        # Calculate books read this year and month
        current_year = datetime.utcnow().year
        current_month = datetime.utcnow().month

        books_read_this_year = sum(
            1 for book in all_books
            if book.read_date and book.read_date.year == current_year
        )

        books_read_this_month = sum(
            1 for book in all_books
            if book.read_date and book.read_date.year == current_year
            and book.read_date.month == current_month
        )

        return LibraryStatsResponse(
            total_books=total_books,
            read_books=read_books,
            unread_books=total_books - read_books,
            favorite_books=favorite_books,
            total_reading_lists=len(reading_lists),
            average_rating=average_rating,
            books_read_this_year=books_read_this_year,
            books_read_this_month=books_read_this_month
        )
