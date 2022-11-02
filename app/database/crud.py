from this import d
from sqlalchemy.orm import Session
from . import schemas, models
from fastapi import HTTPException
from  sqlalchemy.exc import SQLAlchemyError


def get_user_by_username(username: str, db: Session):
    user = db.query(models.Auther).filter(username == models.Auther.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_id(id: int, db: Session):
    user = db.query(models.Auther).filter(id == models.Auther.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(db: Session, user: schemas.AutherCreate):
    auther = models.Auther(**user.dict())
    try:
        db.add(auther)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error

    return auther


def get_all_articles(db: Session):
    return db.query(models.Article).all()


def get_article_by_id(db: Session, id: int):
    article = db.query(models.Article).filter(id == models.Article.id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


def create_article(db: Session, article: schemas.ArticleCreate):
    temp_article = models.Article(**article.dict())
    db.add(temp_article)
    db.commit()
    return temp_article


def get_article_comments(db: Session, article_id: int):
    # ? check if article id is valid
    article = get_article_by_id(db=db, id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    # ? get comments
    comments = (
        db.query(models.Comment).filter(article_id == models.Comment.article_id).all()
    )
    return comments


def create_comment(db: Session, comment: schemas.CommentCreate):
    temp_comment: models.Comment = models.Comment(**comment.dict())
    db.add(temp_comment)
    db.commit()
    return temp_comment
