from crawl4ai import CacheMode, CrawlerRunConfig
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy


def build_url_scraper_config() -> CrawlerRunConfig:
    return CrawlerRunConfig(
        check_robots_txt=True,
        word_count_threshold=100,
        excluded_tags=['script', 'style'],
        exclude_external_links=True,
        exclude_social_media_links=True,
        process_iframes=False,
        remove_overlay_elements=True,
        cache_mode=CacheMode.BYPASS,
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True,
    )
