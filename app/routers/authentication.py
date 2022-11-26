from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from sqlalchemy.exc import SQLAlchemyError

from app.database.crud import create_user
from app.dependencies import authenticate_user, create_access_token
from ..database.main import get_db
from ..database import schemas, crud

auth_router = APIRouter(prefix="/authentication", tags=["Auth"])


@auth_router.post("/register")
async def register_user(user: schemas.AutherCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    if not new_user:
        raise HTTPException(
            status_code=404, detail="user not registered, data is not valid"
        )
    token = create_access_token(
        {"sub": new_user.username}, expires_delta=timedelta(hours=120)
    )

    return {"token": token}


@auth_router.post("/token")
async def login(user: schemas.AutherLogin, db: Session = Depends(get_db)):
    logged_in_user = authenticate_user(db, user.username, user.password)

    if not logged_in_user:

        raise HTTPException(status_code=401, detail="user not found")
    token = create_access_token(
        {"sub": user.username},
        timedelta(hours=120),
    )
    return {
        "token": token
    }


@auth_router.delete("/delete-user")
async def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_user(id, db)

        return {
            "msg": "deleted",

        }
    except SQLAlchemyError as e:
        return {
            "error": e
        }
