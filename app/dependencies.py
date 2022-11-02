from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from typing import Union
from datetime import datetime, timedelta

from .database import models, crud
from .database.main import get_db

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.Auther).filter(models.Auther.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found. username is wrong")

    v_pass = verify_password(password, user.password)
    if v_pass:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found. password is wrong")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        exp = datetime.utcnow() + expires_delta
    else:
        exp = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": exp})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(username, get_db)
    if not user:
        raise HTTPException(status_code=401, detail="Login again, invalid token")
    return user
