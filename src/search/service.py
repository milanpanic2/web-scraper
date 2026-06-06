import asyncio

from duckduckgo_search import DDGS
from sqlalchemy.ext.asyncio import AsyncSession


class SearchService():
    def __init__(self, db: AsyncSession):
        self.db = db


    """
    Sample response from DDGS().text():
    [
        {"title": "Result 1", "href": "https://...", "body": "snippet..."},
        {"title": "Result 2", "href": "https://...", "body": "snippet..."},
    ]
    """
    async def search_with_duck_duck_go(self, search_query: str, max_results: int = 5):
        results = await asyncio.to_thread(DDGS().text, search_query, max_results=max_results)
        return results
