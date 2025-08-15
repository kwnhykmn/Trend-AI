import requests
from bs4 import BeautifulSoup

NAVER_NEWS_URL = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"

def get_naver_news_headlines():
    """
    네이버 경제 뉴스 메인 페이지에서 헤드라인 기사 제목들을 크롤링합니다.
    """
    print("네이버 뉴스 헤드라인 크롤링을 시작합니다...")
    
    try:
        response = requests.get(NAVER_NEWS_URL, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status() # 200 OK가 아니면 에러 발생

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ※ 이 선택자는 웹사이트 구조 변경에 따라 계속 바뀔 수 있습니다.
        # 이전에 'sa_text'로 성공했으므로 그 값을 유지합니다.
        headline_divs = soup.find_all('div', class_='sa_text')

        headlines = []
        for div in headline_divs:
            link = div.find('a')
            if link and link.text.strip():
                title = link.text.strip()
                headlines.append(title)
        
        print(f"총 {len(headlines)}개의 헤드라인을 찾았습니다.")
        return headlines

    except requests.exceptions.RequestException as e:
        print(f"네트워크 오류 발생: {e}")
        return []
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return []