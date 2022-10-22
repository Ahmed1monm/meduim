from typing import List
from pydantic import BaseModel



class ArticlBase(BaseModel):
        body: str
        title: str
        tags: List[str] = []
        


class ArticleCreate(ArticlBase):
        auther_id: int

class Article(ArticleCreate):
        id : int
        class config:
                orm_mode = True



class AutherBase(BaseModel):
        name: str
        title: str
        email: str
        username: str
        bio: str

class AutherCreate(AutherBase):
        password: str

class Auther(AutherBase):
        id: int
        articles: List[Article] = []
        class config:
                orm_mode = True


class CommentBase(BaseModel):
        body: str
        auther_id: int
        article_id: int

class CommentCreate(CommentBase):
        pass

class Comment(CommentBase):
        id: int
        class config:
                orm_mode = True