import requests
from bs4 import BeautifulSoup

NAVER_NEWS_URL = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"

def get_naver_news_headlines():
    print("네이버 뉴스 헤드라인 크롤링을 시작합니다...")
    try:
        response = requests.get(NAVER_NEWS_URL, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Windows 환경에서 테스트했던, 동작이 확인된 선택자 사용
        headline_divs = soup.find_all('div', class_='sa_text')

        headlines = []
        for div in headline_divs:
            link = div.find('a')
            if link and link.text.strip():
                title = link.text.strip()
                headlines.append(title)
        
        print(f"총 {len(headlines)}개의 헤드라인을 찾았습니다.")
        return headlines
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return []