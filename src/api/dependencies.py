import jwt
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import get_db
from src.scraper.service import ScraperService
from src.search.service import SearchService
from src.config import settings


async def get_user_id(request: Request) -> str:
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(401, "Missing token")
    try:
        payload = jwt.decode(auth[7:], settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
    return payload["sub"]
    

async def get_scraper_service(request: Request, db: AsyncSession = Depends(get_db)) -> ScraperService:
    return ScraperService(db=db, scraper_configs=request.app.state.scraper_configs)

async def get_scheduler(request: Request) -> AsyncIOScheduler:
    return request.app.state.scheduler

async def get_search_service(db: AsyncSession = Depends(get_db)) -> SearchService:
    return SearchService(db=db)
