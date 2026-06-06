import asyncio
import json
from collections import defaultdict
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from pathlib import Path
from typing import Final, cast

import aiofiles
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CrawlResult
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ScrapeJob
from src.scraper.config import ScraperType


class ScraperService:
    RESULTS_BASE_DIR: Final[Path] = Path("results")

    def __init__(self, db: AsyncSession, scraper_configs: dict[ScraperType, CrawlerRunConfig]):
        self.db = db
        self.scraper_configs = scraper_configs

    async def create_scrape_job_from_url(self, url: str, user_id: str) -> ScrapeJob:
        # todo - validate url and other stuff before adding and parsing to string
        scrape_job = ScrapeJob(url=url, user_id=user_id)
        self.db.add(scrape_job)
        await self.db.commit()
        await self.db.refresh(scrape_job)
        return scrape_job


    async def scrape_url(self, url: str) -> CrawlResult:
        run_config = self.scraper_configs[ScraperType.SINGLE]
        browser_config = BrowserConfig(verbose=True)

        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = cast(CrawlResult, await crawler.arun(url=url, config=run_config))

            if not result.success:
                raise HTTPException(status_code=500, detail=f"Failed to scrape {url}: {result.error_message}")

            return result

    
    async def scrape_url_bulk(self, urls: list[str]) -> AsyncGenerator[CrawlResult]:
        run_config = self.scraper_configs[ScraperType.SINGLE]
        browser_config = BrowserConfig(verbose=True)

        sem = asyncio.Semaphore(5)
        async with AsyncWebCrawler(config=browser_config) as crawler:
    
            async def scrape_one(url):
                async with sem:
                    return cast(CrawlResult, await crawler.arun(url=url, config=run_config))
            
            tasks = [scrape_one(url) for url in urls]
            for coro in asyncio.as_completed(tasks):
                result = await coro
                yield result


    async def deep_scrape_news_url(self, url: str) -> AsyncGenerator[CrawlResult]:
        run_config = self.scraper_configs[ScraperType.NEWS]
        browser_config = BrowserConfig(verbose=True)

        async with AsyncWebCrawler(config=browser_config) as crawler:
            result_stream = cast(AsyncGenerator[CrawlResult], await crawler.arun(url=url, config=run_config))

            async for result in result_stream:
                if not result.success:
                    print(f"Failed to scrape {result.url}: {result.error_message}")
                    continue

                yield result


    async def scrape_all_news_jobs(self):
        print("Running scheduled scrape for all jobs...")
        sem = asyncio.Semaphore(5)
        stmt = select(ScrapeJob)
        jobs_stream = await self.db.stream_scalars(stmt)

        async def process_job(job: ScrapeJob):
            async with sem:
                async for crawl_result in self.deep_scrape_news_url(job.url):
                    timestamp = datetime.now()
                    # TODO self.RESULTS_BASE_DIR add from k3s
                    directory = self.RESULTS_BASE_DIR / job.url
                    await asyncio.to_thread(directory.mkdir, parents=True, exist_ok=True)
                    filepath = directory / f"{timestamp}.jsonl"
                    line = crawl_result.model_dump_json() + "\n"
                    async with aiofiles.open(filepath, "a") as f:
                        await f.write(line)

        tasks = []
        async for job in jobs_stream:
            tasks.append(asyncio.create_task(process_job(job)))

        # tasks = [ Similar
        #     process_job(job)
        #     async for job in jobs_stream
        # ]

        await asyncio.gather(*tasks)
