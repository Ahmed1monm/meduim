from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Auther(Base):
    __tablename__ = "authers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    title = Column(String)
    bio = Column(String)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    comments = relationship("Comment", back_populates="auther")
    articles = relationship("Article", back_populates="auther")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String, nullable=False)

    auther_id = Column(Integer, ForeignKey("authers.id"))
    article_id = Column(Integer, ForeignKey("articles.id"))

    auther = relationship("Auther", back_populates="comments")
    articles = relationship("Article", back_populates="comments")


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String, nullable=False)
    title = Column(String, nullable=False)

    auther_id = Column(Integer, ForeignKey("authers.id"))
    auther = relationship("Auther", back_populates="articles")
    comments = relationship("Comment", back_populates="articles")


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)


# class ArticleToTags(Base):
#     __tablename__ = 'article_to_tags'
#     __table_args__ = {'extend_existing': True}
#     id = Column(Integer, primary_key=True, index=True)
#
#     article_id = Column(Integer, ForeignKey("articles.id")),
#     tag_id = Column(Integer, ForeignKey("tags.id")),
#
#
# class AuthorsToTags(Base):
#     __tablename__ = 'article_to_tags'
#     __table_args__ = {'extend_existing': True}
#     id = Column(Integer, primary_key=True, index=True)
#     author_id = Column(Integer, ForeignKey("authers.id")),
#     tag_id = Column(Integer, ForeignKey("tags.id")),
