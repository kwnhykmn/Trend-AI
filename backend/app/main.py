from fastapi import FastAPI

# 같은 패키지 내의 모듈들을 임포트
from .database import engine
from . import models
from .routers import users, news

# 애플리케이션 시작 시, models.py에 정의된 모든 테이블을 DB에 생성
models.Base.metadata.create_all(bind=engine)

# FastAPI 앱 인스턴스 생성 및 메타데이터 정의
app = FastAPI(
    title="Trend-AI API",
    description="실시간 소셜 데이터 기반 트렌드 분석 및 예측 AI 서비스 API",
    version="0.1.0",
)

# API 라우터들을 메인 앱에 포함
# 모든 API는 /api/v1 접두사를 가지게 됨
app.include_router(users.router, prefix="/api/v1")
app.include_router(news.router, prefix="/api/v1")

# 서버 동작 확인을 위한 루트 경로
@app.get("/")
def read_root():
    return {"message": "Welcome to Trend-AI API!"}