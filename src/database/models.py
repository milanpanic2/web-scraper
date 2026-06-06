import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ScrapeJob(Base):
    """Model for storing scraping jobs for users."""

    __tablename__ = "scrape_jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    url: Mapped[str] = mapped_column(String(2048), nullable=False, index=True)
    creation_user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_ran_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    group: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    

    def __repr__(self):
        return f"<ScrapeJob(id={self.id}, url={self.url}, creation_user_id={self.creation_user_id})>"
