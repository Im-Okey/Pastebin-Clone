from django.shortcuts import render, get_object_or_404

from ..forms import PasteForm
from ..models import Paste


def handle_post_deletion(request, post, popular_posts):
    """Проверяет, требует ли пост удаление после прочтения."""
    post.views_count += 1
    post.save()

    if post.is_delete_after_read:
        response = render_post_response(request, post, popular_posts, False)
        if post.author != request.user:
            post.delete()
        return response

    return render_post_response(request, post, popular_posts, False)


def render_post_response(request, post, popular_posts, requires_password, error_message=None):
    """Рендерит страницу с постом."""

    likes_count = post.likes_dislikes.filter(action=1).count()
    dislikes_count = post.likes_dislikes.filter(action=-1).count()

    user_liked = post.likes_dislikes.filter(user=request.user, action=1).exists()
    user_disliked = post.likes_dislikes.filter(user=request.user, action=-1).exists()

    form = PasteForm()
    return render(request, 'blog/post.html', {
        'post': post,
        'popular_posts': popular_posts,
        'requires_password': requires_password,
        'error_message': error_message,
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'user_liked': user_liked,
        'user_disliked': user_disliked,
        'form': form
    })


def render_edit_post_response(request, post, popular_posts, error_message=None):
    """Рендерит страницу редактирования поста."""

    likes_count = post.likes_dislikes.filter(action=1).count()
    dislikes_count = post.likes_dislikes.filter(action=-1).count()
    form = PasteForm(instance=post)
    return render(request, 'blog/post.html', {
        'form': form,
        'post': post,
        'popular_posts': popular_posts,
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'error_message': error_message,
    })


def get_post_context(request, slug):
    """Возвращает контекст для поста."""
    post = get_object_or_404(Paste, slug=slug)
    popular_posts = Paste.objects.order_by('-views_count')[:5]

    return post, popular_posts
