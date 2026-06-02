from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import HttpUrl
from starlette.requests import Request
from src.api.schemas import ScrapeRequest, ScrapeJobResponse, ScrapeUrlRequest, SearchRequest
from src.scraper.service import ScraperService
from src.search.service import SearchService
from src.api.dependencies import get_scraper_service, get_user_id, get_search_service


router = APIRouter(prefix="/api/v1", tags=["scraper"])


@router.post("/create-scrape-job", response_model=ScrapeJobResponse)
async def create_scrape_job(
    body: ScrapeRequest,
    user_id: str = Depends(get_user_id),
    scraper_service: ScraperService = Depends(get_scraper_service)):
    job = await scraper_service.create_scrape_job_from_url(str(body.url), user_id)
    return job


@router.post("/scrape-bulk")
async def scrape_bulk(
    body: list[HttpUrl],
    user_id: str = Depends(get_user_id),
    scraper_service: ScraperService = Depends(get_scraper_service)):

    urls = [str(url) for url in body]
    async def stream_results():
        async for result in scraper_service.scrape_url_bulk(urls):
            yield result.model_dump_json() + "\n"

    return StreamingResponse(stream_results(), media_type="application/x-ndjson")


@router.post("/deep-scrape-news-url")
async def deep_scrape_news_url(
    body: ScrapeUrlRequest,
    user_id: str = Depends(get_user_id),
    scraper_service: ScraperService = Depends(get_scraper_service)):

    async def stream_results():
        async for result in scraper_service.deep_scrape_news_url(body.url):
            yield result.model_dump_json() + "\n"
    
    return StreamingResponse(stream_results(), media_type="application/x-ndjson")


@router.post("/search")
async def search_with_duck_duck_go(
    body: SearchRequest,
    user_id: str = Depends(get_user_id),
    search_service: SearchService = Depends(get_search_service)):
    return await search_service.search_with_duck_duck_go(body.search_query, body.max_results)
