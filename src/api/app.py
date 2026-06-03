from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.api.routes import router
from src.database.connection import init_db, AsyncSessionLocal, sync_engine
from src.scraper.service import ScraperService
from src.scraper.config import build_scraper_configs
from src.config.settings import settings
from src.config.telemetry import init_telemetry
from alembic import command
from alembic.config import Config


async def scheduled_scrape_all(scraper_configs):
    async with AsyncSessionLocal() as db:
        try:
            service = ScraperService(db, scraper_configs=scraper_configs)
            await service.scrape_all_news_jobs()
        finally:
            await db.close()


@asynccontextmanager
async def lifespan(fast_api_app: FastAPI):

    init_db()

    # alembic_cfg = Config("alembic.ini")
    # command.upgrade(alembic_cfg, "head")

    init_telemetry(fast_api_app, sync_engine)

    fast_api_app.state.scraper_configs = build_scraper_configs()

    fast_api_app.state.scheduler = AsyncIOScheduler()
    # fast_api_app.state.scheduler.add_job(
    #     func=scheduled_scrape_all,
    #     args=[fast_api_app.state.scraper_configs],
    #     trigger="interval",
    #     hours=12,
    #     id="scrape_all_jobs"
    # )
    fast_api_app.state.scheduler.start()
    print("Scheduler started - scraping every 12 hours")

    yield

    fast_api_app.state.scheduler.shutdown()
    print("Scheduler stopped")


app = FastAPI(
    title="Web Scraper API",
    description="Microservice for web scraping with PostgreSQL storage",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(router)

