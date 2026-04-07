from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


post_tags = Table(
    "post_tags", Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id",  Integer, ForeignKey("tags.id"),  primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50),  unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    bio = Column(Text)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    posts = relationship("Post",    back_populates="author",  cascade="all, delete")
    comments = relationship("Comment", back_populates="author",  cascade="all, delete")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    posts = relationship("Post", back_populates="category")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    excerpt = Column(String(500))
    content = Column(Text, nullable=False)
    cover_image = Column(String(255))
    is_published = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey("users.id"),      nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    author = relationship("User",     back_populates="posts")
    category = relationship("Category", back_populates="posts")
    tags = relationship("Tag",      secondary=post_tags, back_populates="posts")
    comments = relationship("Comment",  back_populates="post", cascade="all, delete")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    post_id = Column(Integer, ForeignKey("posts.id"),     nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"),     nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"),  nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    post = relationship("Post",    back_populates="comments")
    author = relationship("User",    back_populates="comments")
    replies = relationship("Comment", back_populates="parent", cascade="all, delete")
    parent = relationship("Comment", back_populates="replies", remote_side=[id])