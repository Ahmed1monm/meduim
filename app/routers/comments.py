from fastapi import APIRouter, HTTPException
from ..database import schemas, models, crud
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database.main import get_db

comments_router = APIRouter(prefix="/comments", tags=["comments"])


@comments_router.post("/add-comment")
async def add_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    user = db.query(models.Auther).filter(models.Auther.id == comment.auther_id).first()
    article = db.query(models.Article).filter(models.Article.id == comment.article_id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail="user not found please login again"
        )
    if not article:
        raise HTTPException(
            status_code=404, detail="article was deleted"
        )

    n_comment = crud.create_comment(db, comment)
    if not comment:
        raise HTTPException(status_code=400, detail="comment not added")

    return {"comment": comment}


