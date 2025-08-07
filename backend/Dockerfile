# 1. 베이스 이미지(Base Image)를 지정합니다.
# 우리는 Python 3.9 버전을 기반으로 하는 공식 이미지를 사용합니다.
FROM python:3.9-slim

# 2. 작업 디렉토리(Working Directory)를 설정합니다.
# 컨테이너 안에서 명령들이 실행될 기본 경로입니다.
WORKDIR /app

# 3. 의존성 파일을 복사하고 설치합니다.
# 호스트(내 컴퓨터)의 requirements.txt를 컨테이너의 /app/ 안으로 복사합니다.
COPY requirements.txt .

# RUN 명령어로 컨테이너 안에서 셸 명령을 실행합니다.
# pip를 이용해 requirements.txt에 명시된 라이브러리들을 설치합니다.
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드를 복사합니다.
# 호스트의 현재 디렉토리(.)에 있는 모든 파일을 컨테이너의 /app/ 안으로 복사합니다.
COPY . .

# 5. 컨테이너가 시작될 때 실행될 명령(Command)을 지정합니다.
# uvicorn 서버를 실행하여 main.py 안의 app 객체를 실행시킵니다.
# --host 0.0.0.0 옵션은 컨테이너 외부에서 접근 가능하도록 만듭니다.
# --port 8000 옵션은 8000번 포트를 사용하도록 합니다.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]