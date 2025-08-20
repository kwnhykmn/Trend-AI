#CRUD (Create, Read, Update, Delete) 작업을 위한 코드
#이 파일은 데이터베이스와 상호작용하는 함수들을 정의합니다.
# 실제 API를 만들 차례
from sqlalchemy.orm import Session
from . import models, schemas # . 은 같은 폴더를 의미

# 특정 ID로 사용자 조회
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# 이메일로 사용자 조회
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# 새로운 사용자 생성
def create_user(db: Session, user: schemas.UserCreate):
    # 실제로는 비밀번호를 해싱해서 저장해야 함! 지금은 예시로 그대로 저장.
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Update ---
def update_user(db: Session, db_user: models.User, user_update: schemas.UserUpdate):
    # Pydantic 모델에서 받은 데이터 중, 실제 값이 있는 필드만 추출
    update_data = user_update.dict(exclude_unset=True)
    
    # 추출된 데이터로 기존 db_user 객체의 속성을 업데이트
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Delete ---
def delete_user(db: Session, db_user: models.User):
    """
    주어진 사용자 ORM 객체를 데이터베이스에서 삭제합니다.
    """
    db.delete(db_user)
    db.commit()
    # 삭제된 객체를 반환하여 API에서 마지막으로 확인할 수 있게 합니다.
    return db_user

def get_headline_by_title(db: Session, title: str):
    return db.query(models.NewsHeadline).filter(models.NewsHeadline.title == title).first()

def create_news_headline(db: Session, headline: schemas.NewsHeadlineCreate):
    db_headline = models.NewsHeadline(title=headline.title, source=headline.source)
    db.add(db_headline)
    db.commit()
    db.refresh(db_headline)
    return db_headline