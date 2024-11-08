import hashlib
import os
from datetime import timedelta
from typing import Optional, List

from django.db.models import Q
from django.shortcuts import get_object_or_404

from ..models import Tag, Category


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
    need_password = form.cleaned_data.get('need_password')
    stored_password = form.cleaned_data.get('stored_password')

    if need_password:
        password = form.cleaned_data.get('password')
        if password:
            paste.password = hash_password(password)
        elif old_hashed_password:
            paste.password = old_hashed_password
        else:
            form.add_error('password', 'Пароль обязателен, если установлен чекбокс.')
            return True
    else:
        if stored_password:
            paste.password = old_hashed_password
        else:
            paste.password = None

    return False


def get_all_subcategory_ids(category):
    """
    Рекурсивная функция для получения всех id дочерних категорий,
    включая саму категорию.
    """
    category_ids = [category.id]

    for subcategory in category.subcategories.all():
        category_ids.extend(get_all_subcategory_ids(subcategory))

    return category_ids


def sort_and_filter(posts, category, sort_by, access_status, has_password, search_query):
    """
    Фукция выполняющая сортировку и фильтрацию по параметрам
    """

    if category:
        category = get_object_or_404(Category, name=category)
        category_ids = get_all_subcategory_ids(category)
        posts = posts.filter(category__id__in=category_ids)

    if sort_by:
        match sort_by:
            case 'title':
                posts = posts.order_by('title')
            case 'date':
                posts = posts.order_by('-created_at')
            case 'views':
                posts = posts.order_by('-views_count')

    if access_status:
        posts = posts.filter(access_status=access_status)

    if has_password:
        posts = posts.exclude(password__isnull=False).exclude(password__exact='')

    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

    return posts
