# Используем Python 3.12
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем код проекта
COPY . .

# Запуск Celery worker
CMD ["celery", "-A", "config", "worker", "--loglevel=info"]