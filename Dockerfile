FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn requests sqlite3 openai beautifulsoup4 pandas

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]