from fastapi import APIRouter, HTTPException
from ..database import schemas, models, crud
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database.main import get_db
from sqlalchemy.exc import SQLAlchemyError
from app.dependencies import get_current_user

comments_router = APIRouter(prefix="/comments", tags=["comments"])


@comments_router.post("/add-comment")
async def add_comment(comment: schemas.CommentBase, db: Session = Depends(get_db),
                      user: dict = Depends(get_current_user)):
    username = user.get("username")
    temp_user = crud.get_user_by_username(username, db)

    article = db.query(models.Article).filter(models.Article.id == comment.article_id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail="user not found please login again"
        )
    if not article:
        raise HTTPException(
            status_code=404, detail="article was deleted"
        )
    comment_create = schemas.CommentCreate(
        body=comment.body,
        article_id=comment.article_id,
        auther_id=temp_user.id
    )

    n_comment = crud.create_comment(db, comment_create)
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
