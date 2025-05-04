FROM python:3.9-slim

WORKDIR /app

# Устанавливаем зависимости для сборки пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt
RUN pip install --no-cache-dir gunicorn

# Копирование проекта
COPY . .

# Создаем директорию для статических файлов
RUN mkdir -p /app/static /app/media /app/data

CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn auction.wsgi:application --bind 0.0.0.0:8000"]