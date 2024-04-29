from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import requests
import datetime

templates = Jinja2Templates(directory="src/templates")

articles_router = APIRouter()


@articles_router.get("/articles")
async def get_all_articles(
    request: Request,
):
    return templates.TemplateResponse(
        "/articles_table/table.html",
        {
            "request": request,
            "publication": "The Guardian UK",
        },
    )
