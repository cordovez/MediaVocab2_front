from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.database import ArticlesDB, AnalysisDB

router = APIRouter()
templates = Jinja2Templates(directory="templates")


async def _build_articles_context(
    request: Request, db: ArticlesDB, limit: int = 5, skip: int = 0
):
    response = await db.get_articles(limit, skip)

    return {
        "request": request,
        "publication": db.name,
        "count": response.count,
        "articles": response.articles,
    }


# async def _build_full_page_context(
#     request: Request, db: ArticlesDB, limit: int = 5, skip: int = 0
# ):
#     response = await db.get_articles(limit, skip)

#     return {
#         "request": request,
#         "publication": db.name,
#         "count": response.count,
#         "articles": response.articles,
#     }


async def _build_analysis_context(request: Request, db: AnalysisDB, id: str):
    response = await db.get_analysis()
    return {
        "request": request,
        "article_id": response.article_id,
        "verbs": response.verbs,
        "adjectives": response.adjectives,
        "adverbs": response.adverbs,
        "phrases": response.phrases,
        "entities": response.entities,
    }


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------


# @router.get(
#     path="/articles",
#     summary="Gets an HTMX partial for the articles page",
#     tags=["HTMX Partials"],
#     response_class=HTMLResponse,
#     response_model=None,
# )
# async def get_reminders(request: Request, limit: int = 5, skip: int = 0):
#     db = ArticlesDB(name="The Guardian")
#     context = await _build_articles_context(request, db, limit, skip)
#     return templates.TemplateResponse("pages/articles_page.html", context)


@router.get(
    path="/articles-table",
    summary="Returns 'articles.html'",
    tags=["HTMX Partials responses"],
    response_class=HTMLResponse,
    response_model=None,
)
async def get_articles(request: Request, limit: int = 5, skip: int = 0):
    db = ArticlesDB(name="The Guardian")
    context = await _build_articles_context(request, db, limit, skip)
    return templates.TemplateResponse("pages/partials/articles.html", context)


@router.get(
    path="/analysis/{article_id}",
    summary="TBC: Returns text_area.html with content embedded",
    tags=["HTMX Partials"],
    response_class=HTMLResponse,
)
async def get_analysis(request: Request, article_id: str):
    db = AnalysisDB(article_id)
    context = await _build_analysis_context(request, db=db, id=id)
    return templates.TemplateResponse("pages/partials/text_area.html", context)
