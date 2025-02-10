# Базовый образ с Python 3.13
FROM python:3.13-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости и устанавливаем их
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

# Открываем порт для Daphne (обычно 8000)
EXPOSE 8000

# Запускаем Django через Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]