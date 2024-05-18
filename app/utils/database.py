import datetime
import httpx
from pydantic import BaseModel, Field
from typing import Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


class ArticleResponse(BaseModel):
    headline: Optional[str] = None
    teaser: Optional[str] = None
    author: Optional[str] = None
    published: Optional[str] = None
    published_parsed: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    has_analysis: bool = False
    article_id: Optional[str] = Field(None, alias="_id")


class ArticlesResponse(BaseModel):
    count: int
    articles: list[ArticleResponse]


class ArticleDB:
    def __init__(self, id: str) -> None:
        self.id = id

    def _parse_date(self, article):
        # Create a copy of the original article dictionary
        datetime_format = datetime.datetime.strptime(
            article["published"], "%a %d %b %Y %H.%M %Z"
        )
        # parsed_date_string = datetime_format.strftime("%d/%m/%y")
        # article["published_parsed"] = parsed_date_string

        return datetime_format.strftime("%d/%m/%y")

    async def get_article(self) -> ArticleResponse:
        # https://www.youtube.com/watch?v=row-SdNdHFE
        url = f"{BASE_URL}/article/{self.id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        article = response.json()

        return ArticleResponse(**article)


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
        return sorted_articles

    def _parse_date(self, articles):
        parsed_articles = []
        for article in articles:
            # Create a copy of the original article dictionary
            datetime_format = datetime.datetime.strptime(
                article["published"], "%a %d %b %Y %H.%M %Z"
            )
            parsed_date_string = datetime_format.strftime("%d/%m/%y")
            article["published_parsed"] = parsed_date_string
            parsed_articles.append(article)

        return parsed_articles

    def _get_total_count(self):
        pass

    # Public Methods
    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()

    async def get_articles(self, limit: int = 5, skip: int = 0) -> ArticlesResponse:
        # https://www.youtube.com/watch?v=row-SdNdHFE
        url = f"{BASE_URL}/?limit={limit}&skip={skip}"
        count_url = f"{BASE_URL}/count"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            count_response = await client.get(count_url)

        data = response.json()
        articles = data
        count = count_response.json()
        sorted_articles = self._sort_articles(articles)
        parsed_date_articles = self._parse_date(sorted_articles)

        return ArticlesResponse(count=count, articles=parsed_date_articles)


class AnalysisResponse(BaseModel):
    verbs: Optional[list] = None
    adverbs: Optional[list] = None
    adjectives: Optional[list] = None
    entities: Optional[list] = None
    phrases: Optional[list] = None


class AnalysisDB(BaseModel):
    def __init__(self, article_id):
        self.article_id = article_id

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()

    async def get_analysis(self):
        """
        Creates a new analysis document in the collection and returns "1" if successful
        """
        # https://www.youtube.com/watch?v=row-SdNdHFE
        url = f"{BASE_URL}/analysis/{self.article_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response != "1":
            raise "analysis failed"

        data = response.json()
        verbs = data.get("verbs")
        adjectives = data.get("adjectives")
        adverbs = data.get("adverbs")
        phrases = data.get("phrasal_verbs")
        entities = data.get("entities")
        return AnalysisResponse(
            verbs=verbs,
            adjectives=adjectives,
            adverbs=adverbs,
            phrases=phrases,
            entities=entities,
        )
