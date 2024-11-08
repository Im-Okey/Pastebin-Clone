from django.db.models import Q
from django.shortcuts import get_object_or_404

from blog.models import Category
from blog.backends.general_backends import get_all_subcategory_ids


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
