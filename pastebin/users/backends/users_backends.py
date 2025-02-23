import random

from django.db.models import Q
from django.shortcuts import get_object_or_404

from blog.models import Category
from blog.backends.general_backends import get_all_subcategory_ids

from blog.models import Tag

from blog.models import Paste


def sort_and_filter(posts, category, sort_by, access_status, has_password, search_query, selected_tags):
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

    if selected_tags:
        for tag_name in selected_tags:
            posts = posts.filter(tags__name=tag_name)

    return posts


def create_random_pastes(user, num_posts):
    categories = Category.objects.all()
    tags = list(Tag.objects.all())
    for _ in range(num_posts):
        title = f"Post {random.randint(1, 1000)}"
        content = f"This is random content for post {random.randint(1, 1000)}. Some interesting point about {random.choice(tags).name}."

        category = random.choice(categories)
        post_tags = random.sample(tags, random.randint(1, 5))  # Случайное количество тегов

        access_status = random.choice([0, 1, 2])  # Случайный доступ: Private, Public или Draft

        # Время жизни не указываем, чтобы посты не удалялись после просмотра
        time_live = None

        # Создание поста
        post = Paste.objects.create(
            title=title,
            content=content,
            author=user,
            category=category,
            access_status=access_status,
            time_live=time_live,
            views_count=random.randint(10, 500),
        )

        # Добавляем теги к посту
        post.tags.set(post_tags)

        # Опционально добавляем пароль
        if random.choice([True, False]):
            post.password = f"password{random.randint(1000, 9999)}"
            post.save()