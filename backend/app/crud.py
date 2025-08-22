from sqlalchemy.orm import Session

# 같은 패키지 내의 models와 schemas를 상대 경로로 임포트
from . import models, schemas

# --- User CRUD ---

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # 실제 프로덕션에서는 비밀번호를 안전하게 해싱해야 합니다.
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: models.User, user_update: schemas.UserUpdate):
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: models.User):
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