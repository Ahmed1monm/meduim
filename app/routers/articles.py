from fastapi import APIRouter, HTTPException, Depends
from app.database.crud import create_article, get_article_by_id
from ..database.schemas import ArticleCreate
from ..database.main import get_db
from sqlalchemy.orm import Session

article_route = APIRouter(
    prefix="/articles",
    tags=["articles"],
)


@article_route.get("/")
async def get_all_articles():
    articles = get_all_articles
    return {"msg": "Success", "data": articles}


@article_route.post("/add-article")
async def post_article(article: ArticleCreate, db: Session = Depends(get_db)):
    if not article:
        raise HTTPException(status_code=400, detail="Article not posted")
    artic = create_article(db, article)
    if not artic:
        raise HTTPException(status_code=400, detail="Article not posted --")
    return {"msg": "Sucsses", "article added by title": artic.title}


@article_route.get("/{article_id}")
async def get_specific_article(article_id: int, db: Session = Depends(get_db)):
    article = get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"data": article}
