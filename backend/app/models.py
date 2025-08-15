from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

# 같은 패키지 내의 database.py에서 Base를 임포트
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class NewsHeadline(Base):
    __tablename__ = "news_headlines"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    source = Column(String, default="naver_news")
    created_at = Column(DateTime(timezone=True), server_default=func.now())