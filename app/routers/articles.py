from fastapi import APIRouter, HTTPException, Depends
from app.database.crud import create_article, get_article_by_id
from ..database.schemas import ArticleCreate, ArticlBase
from ..database.main import get_db
from sqlalchemy.orm import Session
from ..dependencies import get_current_user
from ..database import models
from ..database import crud
from sqlalchemy.exc import SQLAlchemyError

article_route = APIRouter(
    prefix="/articles",
    tags=["articles"],
)


@article_route.get("/")
async def all_articles(db: Session = Depends(get_db)):
    articles = crud.get_all_articles(db)
    return {"msg": "Success", "data": articles}


@article_route.post("/add-article")
async def post_article(article: ArticlBase, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    temp_user = crud.get_user_by_username(user.get("username"), db)

    if not article:
        raise HTTPException(status_code=400, detail="Article not posted")

    art_create = ArticleCreate(
        title=article.title,
        body=article.body,
        auther_id=temp_user.id)

    artic = create_article(db, art_create)

    if not artic:
        raise HTTPException(status_code=400, detail="Article not posted --")
    return {"msg": "Sucsses", "article added by title": artic.title}


@article_route.get("/{article_id}")
async def get_specific_article(article_id: int, db: Session = Depends(get_db)):
    article = get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"data": article}


@article_route.get("/me/my-articles")
async def get_your_articles(user: dict = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(
            detail="invalid token, login again",
            status_code=400
        )
    try:
        temp_user = crud.get_user_by_username(user.get('username'), db)
        articles = db.query(models.Article).filter(models.Article.auther_id == temp_user.id).all()
        return {
            "msg": "sucsses",
            "data": articles
        }
    except SQLAlchemyError as e:
        return {
            "Error": e
        }


@article_route.delete("/delete")
async def delete_article(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    status = crud.delete_article(id, db)
    if status:
        return {
            "msg": "deleted"
        }
    else:
        raise HTTPException(
            detail="not deleted",
            status_code=500
        )
