from crawl4ai import CrawlerRunConfig, CacheMode, FilterChain, URLPatternFilter, ContentTypeFilter
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy


class NewsScraperConfig(CrawlerRunConfig):
    def __init__(self):
        filter_chain = FilterChain([
            URLPatternFilter(
                patterns=[
                    "*/news/articles/*",
                    "*/news/*",
                ]
            ),
            ContentTypeFilter(allowed_types=["text/html"]),
        ])

        super().__init__(
            check_robots_txt=True,
            word_count_threshold=100,
            excluded_tags=['form', 'button', 'script', 'style', 'footer', "nav", "header"],
            exclude_external_links=True,
            exclude_social_media_links=True,
            process_iframes=False,  # Disable for speed
            remove_overlay_elements=True,
            cache_mode=CacheMode.BYPASS,  # Disable cache to get fresh content
            scraping_strategy=LXMLWebScrapingStrategy(),
            verbose=True,
            stream=True,  # Stream results one by one instead of buffering all in memory
            deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=1,
                max_pages=50,
                include_external=False,
                filter_chain=filter_chain,
            ),
        )
