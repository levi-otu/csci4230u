"""Club models for book clubs."""
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import Base, BaseModel

# Association table for user-club many-to-many relationship
user_clubs = Table(
    "user_clubs",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("club_id", UUID(as_uuid=True), ForeignKey("clubs.id"), primary_key=True),
    Column("join_date", DateTime, default=datetime.utcnow, nullable=False),
    Column("role", String(50), default="member", nullable=False),
)


class Club(BaseModel):
    """Club model for book clubs."""

    __tablename__ = "clubs"

    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    topic = Column(String(255), nullable=True, index=True)
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    is_active = Column(Boolean, default=True, nullable=False)
    max_members = Column(Integer, nullable=True)

    # Relationships
    members = relationship(
        "User",
        secondary=user_clubs,
        back_populates="clubs"
    )
    creator = relationship("User", foreign_keys=[created_by])
    club_meetings = relationship(
        "ClubMeeting",
        back_populates="club",
        cascade="all, delete-orphan"
    )


class ClubMeeting(BaseModel):
    """Club meeting model for recurring club meetings."""

    __tablename__ = "club_meetings"

    club_id = Column(
        UUID(as_uuid=True),
        ForeignKey("clubs.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    meeting_id = Column(
        UUID(as_uuid=True),
        ForeignKey("meetings.id"),
        nullable=False,
        index=True
    )
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    frequency = Column(
        String(50),
        nullable=False,
        default="once"
    )  # once, daily, weekly, monthly
    recurrence_rule = Column(String(500), nullable=True)  # iCal RRULE format

    # Relationships
    club = relationship("Club", back_populates="club_meetings")
    meeting = relationship("Meeting", back_populates="club_meetings")
