from fastapi import APIRouter, HTTPException, Depends
from app.database.crud import create_article, get_article_by_id, get_all_articles
from ..database.schemas import ArticleCreate
from ..database.main import get_db
from sqlalchemy.orm import Session
from ..dependencies import get_current_user
from ..database import models
from ..database import crud

article_route = APIRouter(
    prefix="/articles",
    tags=["articles"],
)


@article_route.get("/")
async def all_articles(db: Session = Depends(get_db)):
    articles = crud.get_all_articles(db)
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


@article_route.get("/your-articles")
async def get_your_articles(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(
            detail="invalid token, login again",
            status_code=400
        )
    articles = db.query(models.Article).filter(models.Article.auther_id == user.get("id")).all()
    return {
        "msg": "sucsses",
        "data": articles
    }


@article_route.delete("/delete")
async def delete_article(id: int, db: Session = Depends(get_db)):
    status = delete_article(id, db)
    if status:
        return {
            "msg": "deleted"
        }
    else:
        raise HTTPException(
            detail="not deleted",
            status_code=500
        )
