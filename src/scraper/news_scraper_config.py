from crawl4ai import CrawlerRunConfig, CacheMode, FilterChain, URLPatternFilter, ContentTypeFilter
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy


def build_news_scraper_config() -> CrawlerRunConfig:
    filter_chain = FilterChain([
        URLPatternFilter(
            patterns=[
                "*/news/articles/*",
                "*/news/*",
            ]
        ),
        ContentTypeFilter(allowed_types=["text/html"]),
    ])

    return CrawlerRunConfig(
        check_robots_txt=True,
        word_count_threshold=100,
        excluded_tags=['form', 'button', 'script', 'style', 'footer', "nav", "header"],
        exclude_external_links=True,
        exclude_social_media_links=True,
        process_iframes=False,
        remove_overlay_elements=True,
        cache_mode=CacheMode.BYPASS,
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True,
        stream=True,
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=1,
            max_pages=50,
            include_external=False,
            filter_chain=filter_chain,
        ),
    )
