import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

# Airflow 컨테이너 내부에서 우리 프로젝트 코드를 찾기 위한 경로 설정
import sys
sys.path.append('/opt/airflow/store')

# 경로 설정 후, 우리 앱의 모듈들을 임포트
from app import crawlers, crud, schemas
from app.database import SessionLocal

def crawl_and_save_headlines():
    """뉴스를 크롤링하고, 중복되지 않은 경우에만 DB에 저장하는 함수"""
    print("뉴스 헤드라인 크롤링 및 저장을 시작합니다.")
    
    headlines_titles = crawlers.get_naver_news_headlines()
    if not headlines_titles:
        print("새로운 뉴스가 없습니다. 작업을 종료합니다.")
        return

    db = SessionLocal()
    saved_count = 0
    try:
        for title in headlines_titles:
            # 중복 헤드라인인지 확인 (crud.py의 함수 이름 확인!)
            existing_headline = crud.get_headline_by_title(db, title=title)
            
            if not existing_headline:
                headline_data = schemas.NewsHeadlineCreate(title=title)
                crud.create_news_headline(db, headline=headline_data)
                saved_count += 1
    finally:
        db.close()
        
    print(f"총 {saved_count}개의 새로운 헤드라인을 저장했습니다.")

with DAG(
    dag_id="naver_news_crawling_dag",
    schedule="@daily",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["crawling", "news"],
) as dag:
    
    crawl_and_save_task = PythonOperator(
        task_id="crawl_and_save_headlines",
        python_callable=crawl_and_save_headlines,
    )