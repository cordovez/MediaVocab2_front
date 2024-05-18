"""
This module provides routes for the analysis partials.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------
from utils.database import AnalysisDB
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# ------------------------------------------------------------------------------
# Templates
# ------------------------------------------------------------------------------

templates = Jinja2Templates(directory="templates")

# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter(prefix="/articles")


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------


async def _build_analysis_context(request: Request, db: AnalysisDB, article_id: str):
    response = await db.get_analysis(article_id)

    return {
        "request": request,
        "analysis": response,
    }


# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------


# @router.get(
#     path="/analysis/{article_id}",
#     summary="Gets the analysis for an existing opinion article",
#     tags=["Partials"],
#     response_class=HTMLResponse,
#     response_model=None,
# )
# async def get_articles(request: Request, db: AnalysisDB, article_id: str):
#     context = _build_analysis_context(request, AnalysisDB(article_id))
#     return templates.TemplateResponse("pages/articles_page.html", context)
