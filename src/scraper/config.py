from enum import StrEnum

from crawl4ai import CrawlerRunConfig

from src.scraper.news_scraper_config import build_news_scraper_config
from src.scraper.url_scraper_config import build_url_scraper_config


class ScraperType(StrEnum):
    NEWS = "news"
    SINGLE = "single"


def build_scraper_configs() -> dict[ScraperType, CrawlerRunConfig]:
    return {
        ScraperType.NEWS: build_news_scraper_config(),
        ScraperType.SINGLE: build_url_scraper_config(),
    }
