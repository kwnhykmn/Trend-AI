from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# 현재 폴더 구조에 맞게 import 경로 수정
import crud
import schemas
from database import SessionLocal

# APIRouter 인스턴스 생성
router = APIRouter(
    prefix="/users", # 이 라우터에 포함된 모든 경로는 /users로 시작
    tags=["users"], # FastAPI 문서에서 API들을 "users" 그룹으로 묶어줌
)

# Dependency (의존성 주입을 위한 함수)
def get_db():
    db = SessionLocal()
    try:
        yield db # 데이터베이스 세션을 생성하고 반환
    finally:
        db.close() # 세션을 닫아 리소스 해제