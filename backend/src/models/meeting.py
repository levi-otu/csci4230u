"""Meeting models for scheduling meetings."""
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class Meeting(BaseModel):
    """Meeting model for both club and user meetings."""

    __tablename__ = "meetings"

    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(
        String(50),
        nullable=False,
        default="scheduled"
    )  # scheduled, in_progress, completed, cancelled
    scheduled_start = Column(DateTime, nullable=False)
    scheduled_end = Column(DateTime, nullable=False)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=False)  # Duration in minutes
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    club_id = Column(
        UUID(as_uuid=True),
        ForeignKey("clubs.id"),
        nullable=True
    )

    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    club = relationship("Club", foreign_keys=[club_id])
    club_meetings = relationship(
        "ClubMeeting",
        back_populates="meeting",
        cascade="all, delete-orphan"
    )
