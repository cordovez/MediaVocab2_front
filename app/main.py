from fastapi import FastAPI, Request
from routers import root_routes, articles_routes, partials_routes, analysis_routes

from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import HTTPException
import uvicorn

# ------------------------------------------------------------------------------
# App Creation
# ------------------------------------------------------------------------------

app = FastAPI()
app.include_router(root_routes.router)
app.include_router(articles_routes.router)
app.include_router(partials_routes.router)
app.include_router(analysis_routes.router)

# ------------------------------------------------------------------------------
# Static Files
# ------------------------------------------------------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")

# ------------------------------------------------------------------------------
# Exception Handlers
# ------------------------------------------------------------------------------


@app.exception_handler(404)
async def page_not_found_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse("/not-found")


# ------------------------------------------------------------------------------
# OpenAPI Customization
# ------------------------------------------------------------------------------


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    description = """MediaVocabulary is an app for exploring various aspects of vocabulary use in contemporary newspaper opinion articles, which may reflect a more conversational tone than reporting articles.
    """

    openapi_schema = get_openapi(
        title="MediaVocabulary App",
        version="1.0.0",
        description=description,
        routes=app.routes,
        tags=[
            {
                "name": "API",
                "description": "Backend API routes for managing article lists and items.",
            },
            {
                "name": "Pages",
                "description": "The main MediaVocabulary web pages.",
            },
            {
                "name": "Authentication",
                "description": "Routes for logging into and out of the app.",
            },
            {
                "name": "HTMX Partials",
                "description": "Routes that serve partial web page contents for HTMX-based requests.",
            },
        ],
    )

    openapi_schema["info"]["x-logo"] = {"url": "static/img/logos/logo.png"}

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(reload=True, app="main:app", port=3000)
