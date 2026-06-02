from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import get_db
from src.scraper.service import ScraperService
from src.search.service import SearchService


async def get_user_id(request: Request) -> str:
    user_id = request.headers.get("x-user-id")
    if not user_id:
        raise HTTPException(status_code=403, detail="Missing x-user-id header")
    return user_id

async def get_scraper_service(request: Request, db: AsyncSession = Depends(get_db)) -> ScraperService:
    return ScraperService(db=db, scraper_configs=request.app.state.scraper_configs)

async def get_scheduler(request: Request) -> AsyncIOScheduler:
    return request.app.state.scheduler

async def get_search_service(db: AsyncSession = Depends(get_db)) -> SearchService:
    return SearchService(db=db)
