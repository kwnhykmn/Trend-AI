import os 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

# 1. .env 파일에서 환경 변수 로드
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 2. 데이터베이스 연결 URL 생성
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 3. SQLAlchemy 엔진 생성
# create_engine 함수는 DB와 연결을 설정하는 시작점
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4. 데이터베이스 세션 생성
# SessionLocal 클래스는 데이터베이스 세션의 인스턴스(생성자)를 만듭니다.
# 각 세션은 DB와 대화하는 창구 역할을 합니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. ORM 모델의 기본 클래스 생성
# 앞으로 우리가 만들 DB 테이블 모델 (e.g., User, Post 등)들은 모두 이 Base 클래스를 상속 받아야 합니다.
Base = declarative_base()