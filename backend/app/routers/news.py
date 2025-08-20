from fastapi import APIRouter, HTTPException
from typing import List

# crawlers 모듈에서 get_naver_news_headlines 함수를 임포트
from .. import crawlers

# APIRouter 인스턴스 생성
router = APIRouter(
    prefix="/news",  # 이 라우터의 모든 경로는 /news 로 시작
    tags=["news"],     # FastAPI 문서에서 "news" 그룹으로 묶어줌
)

@router.get("/headlines", response_model=List[str])
def get_news_headlines():
    """
    네이버 경제 뉴스 헤드라인을 실시간으로 크롤링하여 반환합니다.
    """
    try:
        # 크롤러 함수 호출
        headlines = crawlers.get_naver_news_headlines()

        if not headlines:
            # 크롤링 결과가 비어있을 경우, 503 Service Unavailable 에러를 발생
            raise HTTPException(
                status_code=503, 
                detail="뉴스를 가져올 수 없습니다. 외부 사이트의 문제일 수 있습니다."
            )
        
        return headlines
    
    except Exception as e:
        # 크롤링 중 예상치 못한 에러가 발생했을 경우
        raise HTTPException(
            status_code=500,
            detail=f"서버 내부 오류 발생: {e}"
        )