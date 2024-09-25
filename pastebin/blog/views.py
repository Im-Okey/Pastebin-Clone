from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PasteForm

from .backends.paste_backends import process_time_live, add_tags_to_paste, hash_password, verify_password
from .models import Paste


# ----------------------------------------------------------------------------
# main page
def index(request):
    form = PasteForm()
    popular_posts = Paste.objects.order_by('-views_count')[:5]
    return render(request, 'blog/index.html', {
        'form': form,
        'popular_posts': popular_posts
    })


def posts_check(request):
    posts = Paste.objects.all()
    popular_posts = Paste.objects.order_by('-views_count')[:5]
    return render(request, 'blog/posts.html', {
        'posts': posts,
        'popular_posts': popular_posts
    })


# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# tags
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# comments
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# categories
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# posts

@login_required
def create_paste(request):
    if request.method == 'POST':
        form = PasteForm(request.POST)
        if form.is_valid():
            paste = form.save(commit=False)
            paste.author = request.user

            time_live_value = form.cleaned_data.get('time_live')
            paste.time_live = process_time_live(time_live_value)

            password = form.cleaned_data.get('password')
            if password:
                paste.password = hash_password(password)

            paste.save()

            tags_input = form.cleaned_data['tags']
            add_tags_to_paste(paste, tags_input)

            return redirect('/')
    else:
        form = PasteForm()

    return render(request, 'blog/index.html', {'form': form})


def delete_paste(request, pk):
    post = get_object_or_404(Paste, id=pk)  # Получаем пост по его ID

    if request.method == 'POST':
        post.delete()  # Удаляем пост
        return redirect('users:posts-list')  # Перенаправляем на список постов

    # Для GET-запроса можно вернуть страницу подтверждения удаления (необязательно)
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def detail_post(request, slug):
    post = get_object_or_404(Paste, slug=slug)
    popular_posts = Paste.objects.order_by('-views_count')[:5]

    # Проверка, требует ли пост пароль
    requires_password = bool(post.password)

    # Если пост требует пароль и это GET запрос, просто рендерим страницу
    if requires_password and request.method == 'GET':
        return render_post_response(request, post, popular_posts, requires_password)

    # Если POST запрос и не требуется пароль, просто рендерим пост
    if request.method == 'POST' and not requires_password:
        return handle_post_deletion(request, post, popular_posts)

    return render_post_response(request, post, popular_posts, requires_password)


def post_password_check(request, slug):
    post = get_object_or_404(Paste, slug=slug)
    popular_posts = Paste.objects.order_by('-views_count')[:5]

    if request.method == 'POST':
        entered_password = request.POST.get('password')

        # Проверка пароля
        if verify_password(post.password, entered_password):
            post.views_count += 1
            post.save()
            return handle_post_deletion(request, post, popular_posts)

        # Если пароль неверный, возвращаем сообщение об ошибке
        return render_post_response(request, post, popular_posts, True, "Неверный пароль. Пожалуйста, попробуйте снова.")

    return redirect('blog:post-detail', slug=slug)


def render_post_response(request, post, popular_posts, requires_password, error_message=None):
    return render(request, 'blog/post.html', {
        'post': post,
        'popular_posts': popular_posts,
        'requires_password': requires_password,
        'error_message': error_message,
    })


def handle_post_deletion(request, post, popular_posts):
    # Увеличиваем счётчик просмотров и проверяем, нужно ли удалять пост
    post.views_count += 1
    post.save()

    if post.is_delete_after_read:
        response = render_post_response(request, post, popular_posts, False)
        post.delete()  # Удаляем пост
        return response

    return render_post_response(request, post, popular_posts, False)

# ----------------------------------------------------------------------------
