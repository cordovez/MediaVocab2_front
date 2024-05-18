"""
This module provides routes for the articles pages.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

from utils.database import ArticlesDB, ArticleDB
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# ------------------------------------------------------------------------------
# Templates
# ------------------------------------------------------------------------------

templates = Jinja2Templates(directory="templates")

# ------------------------------------------------------------------------------
# Router
# ------------------------------------------------------------------------------

router = APIRouter()


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------


async def _build_full_page_context(
    request: Request, db: ArticlesDB, limit: int = 5, skip: int = 0
):
    response = await db.get_articles(limit, skip)

    return {
        "request": request,
        "publication": db.name,
        "count": response.count,
        "articles": response.articles,
    }


async def _build_article_context(request: Request, db: ArticleDB, id: str):
    response = await db.get_article()

    return {
        "request": request,
        "article": response,
    }


# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------


@router.get(
    path="/articles",
    summary="Returns the articles_page.html, with pagination and articles.html embedded",
    tags=["Pages"],
    response_class=HTMLResponse,
    response_model=None,
)
async def get_articles(request: Request, limit: int = 5, skip: int = 0):
    context = await _build_full_page_context(
        request, ArticlesDB(name="The Guardian"), limit, skip
    )
    return templates.TemplateResponse("pages/articles_page.html", context)


@router.get(path="/article/{id}", tags=["Pages"])
async def get_article(request: Request, id: str):
    db = ArticleDB(id)
    context = await _build_article_context(request, db, id)
    return templates.TemplateResponse("pages/article_page.html", context)
