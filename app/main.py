from fastapi import FastAPI
from app.routers.comments import comments_router
from app.routers.authentication import auth_router
from app.routers.articles import article_route

app = FastAPI()

app.include_router(article_route)
app.include_router(auth_router)
app.include_router(comments_router)
