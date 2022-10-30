from fastapi import FastAPI
from .routers.articles import article_route

app = FastAPI()

app.include_router(article_route)