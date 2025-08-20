from pydantic import BaseModel, ConfigDict
from typing import Optional # Optional 임포트
from datetime import datetime

# --- User 스키마 ---

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool

    # 이 부분이 반드시 있어야 합니다!
    model_config = ConfigDict(from_attributes=True)  # Pydantic 모델을 SQLAlchemy 모델로 변환할 수 있도록 설정

    # # SQLAlchemy 모델을 Pydantic 모델로 변환할 수 있도록 설정
    # class Config:
    #     orm_mode = True

