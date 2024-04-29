from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import requests
import datetime


def app_context(request: Request):
    return {"app": request.app}


templates = Jinja2Templates(directory="src/templates", context_processors=[app_context])

home_router = APIRouter()


async def fetch_articles(limit: int = 5, skip: int = 0):
    url = f"http://localhost:8000/?limit={limit}&skip={skip}"
    response = requests.get(url)
    data = response.json()
    count = data.get("count")
    articles = data.get("articles")
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
    return count, sorted_articles


@home_router.get("/")
async def go_home(request: Request, limit: int = 5, skip: int = 0):
    count, sorted_articles = await fetch_articles(limit, skip)
    return templates.TemplateResponse(
        "home/home.html",
        {"request": request, "count": count, "articles": sorted_articles},
    )


# @home_router.get("/")
# async def go_home(request: Request):
#     limit = 5
#     skip = 0
#     count, articles = await fetch_articles(limit, skip)

#     return templates.TemplateResponse(
#         "layout/_index.html",
#         {
#             "request": request,
#             "publication": "The Guardian UK",
#             "articles": articles,
#             "total_articles": count,
#         },
#     )


# @home_router.get("/articles")
# async def get_all_articles(
#     request: Request,
# ):
#     limit = 5
#     skip = 0

#     count, articles = await fetch_articles(limit, skip)
#     return templates.TemplateResponse(
#         "/articles_table/table.html",
#         {
#             "request": request,
#             "publication": "The Guardian UK",
#             "articles": articles,
#             "total_articles": count,
#         },
#     )
