import hashlib
import os
from datetime import timedelta
from typing import Optional, List

from ..models import Tag


def process_time_live(time_live_value: Optional[str]) -> Optional[timedelta]:
    """Функция для обработки значения времени жизни."""
    if time_live_value and time_live_value != "None":
        try:
            time_live_seconds = float(time_live_value)
            return timedelta(seconds=time_live_seconds)
        except ValueError:
            return None
    return None


def add_tags_to_paste(paste: 'Paste', tags_input: Optional[str]) -> None:
    """Функция для перезаписи тегов у пасты."""
    paste.tags.clear()

    if tags_input:
        tags_list: List[str] = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        for tag_name in tags_list:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            paste.tags.add(tag)


def hash_password(password: str) -> str:
    """Хеширует пароль с использованием SHA-256."""
    salt = os.urandom(16)
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
    return salt.hex() + ':' + hashed_password


def verify_password(stored_password: str, provided_password: str) -> bool:
    """Проверяет, соответствует ли введенный пароль сохраненному хешу."""
    salt, hashed_password = stored_password.split(':')
    return hashed_password == hashlib.sha256(bytes.fromhex(salt) + provided_password.encode()).hexdigest()


def process_time(form):
    """Обрабатывает полученное с формы время удаления"""
    time_live_value = form.cleaned_data.get('time_live')
    return None if time_live_value == 0 else process_time_live(time_live_value)


def handle_password(form, paste, old_hashed_password):
    """Работает с паролем в зависимости от данных полученных с клиента"""
    password = form.cleaned_data.get('password')
    need_password = form.cleaned_data.get('need_password')

    if need_password:
        if password:
            paste.password = hash_password(password)
        else:
            form.add_error('password', 'Пароль обязателен, если установлен чекбокс.')
            return True
    else:
        paste.password = old_hashed_password

    return False