FROM python:3.9

# Устанавливаем postgresql-client для работы wait-for-db.sh
RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

# Добавляем скрипт для проверки готовности базы данных
COPY wait-for-db.sh .
RUN chmod +x wait-for-db.sh

# Добавляем переменные окружения
ENV POSTGRES_DB=foodram \
    POSTGRES_USER=foodram_user \
    POSTGRES_PASSWORD=foodram_password \
    DB_HOST=db \
    DB_PORT=5432

CMD ["./wait-for-db.sh", "db", "5432", "gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]
