import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# .env 파일에서 환경 변수 로드
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 데이터베이스 연결 URL 생성 (PostgreSQL 용)
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy 엔진 생성
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 데이터베이스 세션 생성 클래스
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 모델의 기본이 될 Base 클래스 생성
Base = declarative_base()


# API 의존성 주입을 위한 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()