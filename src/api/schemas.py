from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl, ConfigDict


class ScrapeRequest(BaseModel):
    """Request schema for initiating a scrape."""
    url: HttpUrl


class ScrapeJobResponse(BaseModel):
    """Response schema for scrape job."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    url: str
    user_id: str
    job_name: str
    created_at: datetime
    last_ran_at: Optional[datetime] = None


class ScrapeUrlRequest(BaseModel):
    url: str


class SearchRequest(BaseModel):
    search_query: str
    max_results: int
