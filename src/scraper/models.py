from datetime import datetime

from pydantic import BaseModel


class ScrapedResult(BaseModel):
    url: str
    depth: int
    published_time: datetime
    scraped_at: datetime
    metadata: str
    markdown: str