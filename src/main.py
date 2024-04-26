from fastapi import FastAPI
from views.articles import articles_router
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(articles_router, tags=["The Guardian Opinions"])


if __name__ == "__main__":
    uvicorn.run(reload=True, app="main:app", port=3000)
