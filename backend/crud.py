#CRUD (Create, Read, Update, Delete) 작업을 위한 코드
#이 파일은 데이터베이스와 상호작용하는 함수들을 정의합니다.
# 실제 API를 만들 차례
from sqlalchemy.orm import Session
import models
import schemas 

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