from typing import List
from pydantic import BaseModel


class ArticlBase(BaseModel):
    body: str
    title: str


class ArticleCreate(ArticlBase):
    auther_id: int


class Article(ArticleCreate):
    id: int

    class config:
        orm_mode = True


class AutherBase(BaseModel):
    name: str
    title: str
    email: str
    username: str
    bio: str


class AutherLogin(BaseModel):
    username: str
    password: str


class AutherCreate(AutherBase):
    password: str


class Auther(AutherBase):
    id: int
    articles: List[Article] = []

    class config:
        orm_mode = True


class CommentBase(BaseModel):
    body: str
    article_id: int


class CommentCreate(CommentBase):
    auther_id: int


class Comment(CommentCreate):
    id: int

    class config:
        orm_mode = True


class ArticleToTagsBasic:
    article_id: int
    tag_id: int


class ArticleToTags(ArticleToTagsBasic):
    id: int


class TagBasic:
    id: int
    name: str
