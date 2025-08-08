from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# 현재 폴더 구조에 맞게 import 경로 수정
from .. import crud, schemas
from ..database import SessionLocal, get_db

# APIRouter 인스턴스 생성
router = APIRouter(
    prefix="/users", # 이 라우터에 포함된 모든 경로는 /users로 시작
    tags=["users"], # FastAPI 문서에서 API들을 "users" 그룹으로 묶어줌
)


# # 이제 데코레이터가 @app.post가 아니라 @router.post가 됨
# @router.post("/", response_model=schemas.User) # 사용자 생성 API
# def create_user_api(user: schemas.UserCreate, db: Session = Depends(get_db)): # 의존성 주입을 통해 DB 세션을 가져옴
#     db_user = crud.get_user_by_email(db, email=user.email) # 이메일로 사용자 조회
#     if db_user: # 이미 존재하는 이메일인지 확인
#         raise HTTPException(status_code=400, detail="Email already registered") # 이메일이 이미 등록되어 있으면 예외 발생
#     return crud.create_user(db=db, user=user) # 사용자 생성

# ''''''
# @router.get("/{user_id}", response_model=schemas.User) # 사용자 조회 API
# def read_user_api(user_id: int, db: Session = Depends(get_db)): # 사용자 ID로 조회
#     db_user = crud.get_user(db, user_id=user_id) # CRUD 함수로 사용자 정보 가져오기
#     if db_user is None: # 사용자 정보가 없으면 예외 발생
#         raise HTTPException(status_code=404, detail="User not found") # 사용자 정보를 찾을 수 없으면 404 에러
#     return db_user # 사용자 정보 반환

@router.post("/", response_model=schemas.User)
def create_user_api(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_by_email = crud.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # crud 함수를 호출하여 DB 객체를 받음
    created_user_db_object = crud.create_user(db=db, user=user)
    
    # 💥 핵심: DB 객체를 Pydantic 스키마로 명시적으로 변환하여 반환
    # 이 과정에서 orm_mode=True (from_attributes=True) 설정이 사용됨
    return schemas.User.from_orm(created_user_db_object)

# read_user_api도 동일하게 수정 (예방 차원에서)
@router.get("/{user_id}", response_model=schemas.User)
def read_user_api(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 명시적 변환
    return schemas.User.from_orm(db_user)

# 사용자 업데이트 API
@router.patch("/{user_id}", response_model=schemas.User)
def update_user_api(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 이메일을 변경하려는 경우, 해당 이메일이 이미 사용 중인지 확인
    if user_update.email:
        existing_user = crud.get_user_by_email(db, email=user_update.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=400, detail="Email already registered")

    return crud.update_user(db=db, db_user=db_user, user_update=user_update)

# 사용자 삭제 API
@router.delete("/{user_id}", response_model=schemas.User)
def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db=db, db_user=db_user)