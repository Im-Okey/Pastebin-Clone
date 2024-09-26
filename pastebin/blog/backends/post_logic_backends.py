from django.shortcuts import render


def handle_post_deletion(request, post, popular_posts):
    """Проверяет, требует ли пост удаление после прочтения."""
    post.views_count += 1
    post.save()

    if post.is_delete_after_read:
        response = render_post_response(request, post, popular_posts, False)
        post.delete()
        return response

    return render_post_response(request, post, popular_posts, False)


def render_post_response(request, post, popular_posts, requires_password, error_message=None):
    """Рендерит страницу с постом."""
    return render(request, 'blog/post.html', {
        'post': post,
        'popular_posts': popular_posts,
        'requires_password': requires_password,
        'error_message': error_message,
    })