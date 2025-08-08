from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users # 우리가 만든 users 라우터를 임포트합니다.

# 애플리케이션 시작 시 DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="Trend-AI API",
    description="실시간 소셜 데이터 기반 트렌드 분석 및 예측 AI 서비스 API",
    version="0.1.0",
)

# /api/v1 경로 아래에 users 라우터를 포함시킵니다.
app.include_router(users.router, prefix="/api/v1")


# 서버가 살아있는지 확인하기 위한 기본 루트 경로
@app.get("/")
def read_root():
    return {"message": "Welcome to Trend-AI API!"}