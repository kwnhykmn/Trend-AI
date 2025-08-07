from pydantic import BaseModel

# --- User 스키마 ---

# 사용자 생성을 위한 기본 스키마 (API 요청 시 사용)
class UserCreate(BaseModel):
    email: str
    password: str

# 사용자 조회를 위한 기본 스키마 (API 응답 시 사용)
# password 같은 민감 정보는 포함하지 않음
class User(BaseModel):
    id: int
    email: str
    is_active: bool

    # SQLAlchemy 모델을 Pydantic 모델로 변환할 수 있도록 설정
    class Config:
        orm_mode = True