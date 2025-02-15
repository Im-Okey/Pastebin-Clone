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

# Создаём директорию для статики
RUN mkdir -p /vol/web/static && chmod -R 755 /vol/web/static

# Открываем порт 8000
EXPOSE 8000

# Запуск через Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]