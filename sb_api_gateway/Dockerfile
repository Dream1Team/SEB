# Dockerfile
FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements первыми (для лучшего кэширования)
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

## Делаем скрипты исполняемыми
#RUN chmod +x entrypoint.sh
#
## Инициализируем Alembic
#RUN alembic init alembic
#
## Копируем настроенный env.py (если не генерируется автоматически)
#COPY alembic/env.py alembic/env.py

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Порт приложения
EXPOSE 8003

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]