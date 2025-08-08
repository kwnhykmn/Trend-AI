from pydantic import BaseModel, ConfigDict
from typing import Optional # Optional 임포트

# --- User 스키마 ---

# 사용자 생성을 위한 기본 스키마 (API 요청 시 사용)
class UserCreate(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = None


# 사용자 조회를 위한 기본 스키마 (API 응답 시 사용)
# password 같은 민감 정보는 포함하지 않음
class User(BaseModel):
    id: int
    email: str
    is_active: bool

    # 이 부분이 반드시 있어야 합니다!
    model_config = ConfigDict(from_attributes=True)  # Pydantic 모델을 SQLAlchemy 모델로 변환할 수 있도록 설정

    # # SQLAlchemy 모델을 Pydantic 모델로 변환할 수 있도록 설정
    # class Config:
    #     orm_mode = True

