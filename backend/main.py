from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models # models.py 임포트
import schemas
from database import engine, SessionLocal # database.py 의 engine 객체 임포트


# models.py에 정의된 모든 테이블들을 실제 데이터베이스에 생성
#이미 테이블이 존재하면 아무 작업도 하지 않습니다.
models.Base.metadata.create_all(bind=engine)

#FastAPI 인스턴스 생성
app = FastAPI()

# Dependency (의존성 주입을 위한 함수)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user_api(user: schemas.UserCreate, db: Session = Depends(get_db)): # user: schemas.UserCreate 로 수정
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user_api(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#루트경로 ("/")에 대한 GET 요청이 오면 실행될 함수 정의
@app.get("/")
def read_root():
    return {"Hello":"World"}
