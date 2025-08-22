from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List # List[schemas.User] 와 같이 여러 사용자를 반환하는 API를 위해 추가

# 상위 app 패키지에서 필요한 모듈과 함수를 임포트
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", response_model=schemas.User)
def create_user_api(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    created_user_db_object = crud.create_user(db=db, user=user)
    return schemas.User.from_orm(created_user_db_object)

@router.get("/{user_id}", response_model=schemas.User)
def read_user_api(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.User.from_orm(db_user)

@router.patch("/{user_id}", response_model=schemas.User)
def update_user_api(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.email:
        existing_user = crud.get_user_by_email(db, email=user_update.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=400, detail="Email already registered")

    updated_user_db_object = crud.update_user(db=db, db_user=db_user, user_update=user_update)
    return schemas.User.from_orm(updated_user_db_object)

@router.delete("/{user_id}", response_model=schemas.User)
def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    deleted_user_db_object = crud.delete_user(db=db, db_user=db_user)
    return schemas.User.from_orm(deleted_user_db_object)