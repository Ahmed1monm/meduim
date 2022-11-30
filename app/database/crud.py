from sqlalchemy.orm import Session
from app.database import schemas, models
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.dependencies import AuthDepends


def get_user_by_username(username: str, db: Session):
    user = db.query(models.Auther).filter(username == models.Auther.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def delete_user(u_id: int, db: Session):
    user = get_user_by_id(u_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    try:
        # db.query(models.Auther).filter(models.Auther.id == u_id).delete()
        db.delete(user)
        db.commit()
        return True
    except SQLAlchemyError:
        raise HTTPException(
            status_code=400, detail="Not deleted"
        )


def get_user_by_id(id: int, db: Session):
    user = db.query(models.Auther).filter(id == models.Auther.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(db: Session, user: schemas.AutherCreate):
    pass_hashing = AuthDepends.get_password_hash(user.password)
    user.password = pass_hashing
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


def delete_article(id: int, db: Session):
    article = get_article_by_id(db, id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    try:
        db.delete(article)
        db.commit()
        # db.query(models.Article).filter(models.Article.id == id).delete()
        return True
    except SQLAlchemyError:
        raise HTTPException(
            status_code=400, detail="Not deleted"
        )


def create_comment(db: Session, comment: schemas.CommentCreate):
    temp_comment: models.Comment = models.Comment(**comment.dict())
    db.add(temp_comment)
    db.commit()
    return temp_comment


def get_comment_by_id(id: int, db: Session):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


def delete_comment(db: Session, id: int):
    comment = get_comment_by_id(id, db)
    if not comment:
        raise HTTPException(detail="Comment not found, wrong id", status_code=404)
    try:
        db.delete(comment)
        db.commit()
        return True
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f'ERROR {e}')
