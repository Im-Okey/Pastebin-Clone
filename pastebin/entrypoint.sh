#!/bin/sh

# Применяем миграции
echo "Making migrations..."
python manage.py makemigrations

echo "Applying database migrations..."
python manage.py migrate

# Создаём суперпользователя, если его нет
echo "Creating superuser if not exists..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
EOF

# Собираем статику
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Запускаем основной процесс (например, сервер через Daphne)
exec "$@"