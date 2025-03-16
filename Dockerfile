FROM python:3.11-slim

WORKDIR /app/backend

# 只安裝 poetry
RUN pip install --no-cache-dir poetry

# 複製專案檔案
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "poetry install && cd src/kdan_backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000"]
