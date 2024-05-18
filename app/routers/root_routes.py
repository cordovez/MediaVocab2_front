from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get(
    path="/", summary="Redirects to the login or articles pages", tags=["Pages"]
)
async def read_root():
    cookie = True
    path = "/articles" if cookie else "/login"
    return RedirectResponse(path, status_code=302)


@router.get(path="/favicon.ico", include_in_schema=False)
async def get_favicon():
    return FileResponse("static/img/favicon.ico")


@router.get(path="/not-found", summary='Returns "not-found.html"', tags=["Pages"])
async def get_not_found(request: Request):
    return templates.TemplateResponse("pages/not-found.html", {"request": request})
