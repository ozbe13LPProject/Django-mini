# 베이스 이미지
FROM python:3.11-slim

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/root/.local/bin:/root/.cargo/bin:${PATH}"

# 필수 패키지 설치 (uv 실행 및 빌드 도구 등)
RUN apt-get update \
    && apt-get install -y curl build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# uv 설치
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 작업 디렉토리 설정
WORKDIR /app

# pyproject.toml & uv.lock 복사 및 설치
COPY ./pyproject.toml ./uv.lock ./

#RUN uv sync --all-packages
#RUN uv sync --frozen
#배포시
#RUN uv sync --group prod
RUN uv pip install .[prod] --system

# 애플리케이션 코드 복사
COPY . .

# 포트 설정 (FastAPI일 경우도 동일)
EXPOSE 8000

# Django 개발 서버 실행
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
COPY ./scripts /scripts
RUN chmod +x /scripts/run.sh

CMD ["/scripts/run.sh"]

#이미지빌드
#docker build -t my-django-app:final .
#컨테이너
#docker run -d -p 8000:8000 --name django-final-test my-django-app:final
#로그 확인
#docker logs django-final-test
#기존 컨테이너 삭제
#docker rm -f django-final-test