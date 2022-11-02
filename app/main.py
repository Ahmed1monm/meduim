from fastapi import FastAPI
from .routers.articles import article_route
from .routers.authentication import auth_router
from .routers.comments import comments_router

app = FastAPI()

app.include_router(article_route)
app.include_router(auth_router)
app.include_router(comments_router)
