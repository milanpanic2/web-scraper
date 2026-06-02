from enum import StrEnum

from crawl4ai import CrawlerRunConfig

from src.scraper.news_scraper_config import NewsScraperConfig
from src.scraper.url_scraper_config import UrlScraperConfig


class ScraperType(StrEnum):
    NEWS = "news"
    SINGLE = "single"


def build_scraper_configs() -> dict[ScraperType, CrawlerRunConfig]:
    return {
        ScraperType.NEWS: NewsScraperConfig(),
        ScraperType.SINGLE: UrlScraperConfig(),
    }
