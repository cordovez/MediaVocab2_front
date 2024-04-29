import datetime
import httpx
from pydantic import BaseModel
from typing import Optional, Any


class Article(BaseModel):
    _id: Optional[str] = None
    headline: Optional[str] = None
    teaser: Optional[str] = None
    author: Optional[str] = None
    published: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    has_analysis: bool = False


class ArticlesResponse(BaseModel):
    count: int
    articles: list[Article]


class ArticlesDB:
    def __init__(self, name: str = "The Guardian") -> None:
        self.name = name

    # Private Methods
    def _sort_articles(self, articles):
        # ignore articles without dates and sort
        articles_with_date = [
            article for article in articles if article.get("published")
        ]
        sorted_articles = sorted(
            articles_with_date,
            key=lambda article: (
                datetime.datetime.strptime(article["published"], "%a %d %b %Y %H.%M %Z")
            ),
            reverse=True,
        )
        for article in sorted_articles:
            article_date = datetime.datetime.strptime(
                article["published"], "%a %d %b %Y %H.%M %Z"
            )
            article["published"] = article_date.strftime("%d/%m/%y")
        return sorted_articles

    def _get_total_count(self):
        pass

    # Public Methods
    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()

    async def get_articles(self, limit: int = 5, skip: int = 0) -> ArticlesResponse:
        # https://www.youtube.com/watch?v=row-SdNdHFE
        url = f"http://localhost:8000/?limit={limit}&skip={skip}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        # response = requests.get(url)
        data = response.json()
        articles = data.get("articles")
        count = data.get("count")
        sorted_articles = self._sort_articles(articles)

        return ArticlesResponse(count=count, articles=sorted_articles)
