from fastapi import APIRouter, HTTPException
from ..database import schemas, models, crud
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database.main import get_db
from sqlalchemy.exc import SQLAlchemyError

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
    if not n_comment:
        raise HTTPException(status_code=400, detail="comment not added")

    return {"comment": n_comment}


@comments_router.delete('/delete-comment')
async def delete_comment(id: int, db: Session = Depends(get_db)):
    status = crud.delete_comment(db, id)
    if status:
        return {
            'status': True,
            'msg': "deleted"
        }
