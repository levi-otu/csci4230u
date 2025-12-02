"""Simple schema instantiation tests for coverage."""
from datetime import datetime
from uuid import uuid4

# Import all schemas to test them
from src.transports.json.book_schemas import (
    PublisherCreate, PublisherUpdate, PublisherResponse,
    BookCreate, BookUpdate, BookResponse,
    BookVersionCreate, BookVersionUpdate, BookVersionResponse
)

from src.transports.json.meeting_schemas import (
    MeetingCreate, MeetingUpdate, MeetingResponse
)

from src.transports.json.page_schemas import (
    PageCreate, PageUpdate, PageResponse
)


# Book schemas
def test_publisher_create():
    """Test PublisherCreate schema."""
    p = PublisherCreate(name="Test Pub")
    assert p.name == "Test Pub"


def test_publisher_update():
    """Test PublisherUpdate schema."""
    p = PublisherUpdate(name="Updated")
    assert p.name == "Updated"


def test_publisher_response():
    """Test PublisherResponse schema."""
    p = PublisherResponse(
        id=uuid4(), name="Pub", country=None, website=None,
        created_at=datetime.now(), updated_at=datetime.now()
    )
    assert p.name == "Pub"


def test_book_create():
    """Test BookCreate schema."""
    b = BookCreate(title="Book", author="Author")
    assert b.title == "Book"


def test_book_update():
    """Test BookUpdate schema."""
    b = BookUpdate(title="Updated")
    assert b.title == "Updated"


def test_book_response():
    """Test BookResponse schema."""
    b = BookResponse(
        id=uuid4(), title="Book", author="Author",
        date_of_first_publish=None, genre=None, description=None,
        created_at=datetime.now(), updated_at=datetime.now()
    )
    assert b.title == "Book"


def test_book_version_create():
    """Test BookVersionCreate schema."""
    bv = BookVersionCreate(
        book_id=uuid4(), isbn="1234567890"
    )
    assert bv.isbn == "1234567890"


def test_book_version_update():
    """Test BookVersionUpdate schema."""
    bv = BookVersionUpdate(isbn="0987654321")
    assert bv.isbn == "0987654321"


def test_book_version_response():
    """Test BookVersionResponse schema."""
    bv = BookVersionResponse(
        id=uuid4(), book_id=uuid4(), publisher_id=None,
        isbn="1234567890", publish_date=None, edition=None,
        editors=None, editor_info=None,
        created_at=datetime.now(), updated_at=datetime.now()
    )
    assert bv.isbn == "1234567890"


# Meeting schemas
def test_meeting_create():
    """Test MeetingCreate schema."""
    m = MeetingCreate(
        name="Meeting",
        scheduled_start="2024-12-01T10:00:00",
        scheduled_end="2024-12-01T11:00:00",
        duration=60
    )
    assert m.name == "Meeting"


def test_meeting_update():
    """Test MeetingUpdate schema."""
    m = MeetingUpdate(name="Updated Meeting")
    assert m.name == "Updated Meeting"


def test_meeting_response():
    """Test MeetingResponse schema."""
    m = MeetingResponse(
        id=uuid4(), name="Meeting",
        description=None,
        scheduled_start="2024-12-01T10:00:00",
        scheduled_end="2024-12-01T11:00:00",
        duration=60, status="scheduled",
        actual_start=None, actual_end=None,
        created_by=uuid4(), club_id=None,
        created_at=datetime.now(), updated_at=datetime.now()
    )
    assert m.name == "Meeting"


# Page schemas
def test_page_create():
    """Test PageCreate schema."""
    p = PageCreate(name="Page", description=None, topic=None)
    assert p.name == "Page"


def test_page_update():
    """Test PageUpdate schema."""
    p = PageUpdate(name="Updated Page")
    assert p.name == "Updated Page"


def test_page_response():
    """Test PageResponse schema."""
    p = PageResponse(
        id=uuid4(), name="Page",
        description=None, topic=None,
        created_by=uuid4(), is_active=True,
        created_at=datetime.now(), updated_at=datetime.now()
    )
    assert p.name == "Page"
