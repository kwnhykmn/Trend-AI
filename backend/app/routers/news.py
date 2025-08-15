from fastapi import APIRouter, HTTPException
from typing import List

from .. import crawlers

router = APIRouter(
    prefix="/news",
    tags=["news"],
)

@router.get("/headlines", response_model=List[str])
def get_news_headlines():
    """
    네이버 경제 뉴스 헤드라인을 실시간으로 크롤링하여 반환합니다.
    """
    try:
        headlines = crawlers.get_naver_news_headlines()
        if not headlines:
            raise HTTPException(status_code=503, detail="뉴스를 가져올 수 없습니다.")
        return headlines
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 내부 오류 발생: {e}")