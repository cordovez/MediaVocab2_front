from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.database import ArticlesDB

router = APIRouter()
templates = Jinja2Templates(directory="templates")


async def _build_full_page_context(
    request: Request, db: ArticlesDB, limit: int = 5, skip: int = 0
):
    response = await db.get_articles(limit, skip)

    return {
        "request": request,
        # "publication": db.name,
        # "count": response.count,
        "articles": response.articles,
    }


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------


@router.get(
    path="/articles-table",
    summary="Gets an HTMX partial for the articles page",
    tags=["HTMX Partials"],
    response_class=HTMLResponse,
    response_model=None,
)
async def get_reminders(request: Request, limit: int = 5, skip: int = 0):
    db = ArticlesDB(name="The Guardian")
    context = await _build_full_page_context(request, db, limit, skip)
    return templates.TemplateResponse("pages/partials/articles_table.html", context)
