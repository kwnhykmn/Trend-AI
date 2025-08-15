from pydantic import BaseModel, ConfigDict
from typing import Optional
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

    # Pydantic V2 스타일에 맞는 ORM 설정
    model_config = ConfigDict(from_attributes=True)


# --- NewsHeadline 스키마 ---

class NewsHeadlineBase(BaseModel):
    title: str
    source: Optional[str] = "naver_news"

class NewsHeadlineCreate(NewsHeadlineBase):
    pass

class NewsHeadline(NewsHeadlineBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)