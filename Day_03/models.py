from sqlalchemy import Column, Integer, String, ForeignKey,func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100), unique=True, index=True)

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"

    # Relationship with posts
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship back to user
    author = relationship("User", back_populates="posts")
