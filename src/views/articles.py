from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import requests
import datetime

templates = Jinja2Templates(directory="src/templates")

articles_router = APIRouter()


@articles_router.get("/articles")
async def get_all_articles(request: Request):
    response = requests.get("http://localhost:8000/")
    data = response.json()
    count = data.get("count")
    articles = data.get("articles")
    print(data)

    articles_with_date = [article for article in articles if article.get("published")]

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

    return templates.TemplateResponse(
        "layout/index.html",
        {
            "request": request,
            "publication": "The Guardian UK",
            "articles": sorted_articles,
            "total_articles": count,
        },
    )
