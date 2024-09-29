from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PasteForm

from .backends.general_backends import process_time_live, add_tags_to_paste, hash_password, verify_password
from .backends.post_logic_backends import handle_post_deletion, render_post_response

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
            paste.time_live = process_time_live(time_live_value)  # Преобразуем секунды в timedelta

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
    post = get_object_or_404(Paste, id=pk)

    if request.method == 'POST':
        post.delete()  # Удаляем пост
        return redirect('users:posts-list')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Paste, slug=slug, author=request.user)
    popular_posts = Paste.objects.order_by('-views_count')[:5]

    if request.method == 'POST':
        form = PasteForm(request.POST, instance=post)
        if form.is_valid():
            paste = form.save(commit=False)

            time_live_value = form.cleaned_data.get('time_live')
            if time_live_value == 0:
                paste.time_live = None
            else:
                paste.time_live = process_time_live(time_live_value)

            password = form.cleaned_data.get('password')
            need_password = form.cleaned_data.get('need_password')

            if need_password:
                if password:
                    paste.password = hash_password(password)
                else:
                    paste.password = post.password
            else:
                paste.password = post.password

            paste.save()

            tags_input = form.cleaned_data['tags']
            add_tags_to_paste(paste, tags_input)

            return render_post_response(request, post, popular_posts, requires_password=False)
    else:
        form = PasteForm(instance=post)

    return render(request, 'post.html', {'form': form, 'post': post, 'popular_posts': popular_posts})


def detail_post(request, slug):
    post = get_object_or_404(Paste, slug=slug)
    popular_posts = Paste.objects.order_by('-views_count')[:5]

    requires_password = bool(post.password)

    if requires_password and request.method == 'GET':
        return render_post_response(request, post, popular_posts, requires_password)

    if request.method == 'GET' and not requires_password:
        return handle_post_deletion(request, post, popular_posts)

    return render_post_response(request, post, popular_posts, requires_password)


def post_password_check(request, slug):
    post = get_object_or_404(Paste, slug=slug)
    popular_posts = Paste.objects.order_by('-views_count')[:5]

    if request.method == 'POST':
        entered_password = request.POST.get('password')

        if verify_password(post.password, entered_password):
            post.views_count += 1
            post.save()
            return handle_post_deletion(request, post, popular_posts)

        return render_post_response(request, post, popular_posts, True,
                                    "Неверный пароль. Пожалуйста, попробуйте снова.")

    return redirect('blog:post-detail', slug=slug)

# ----------------------------------------------------------------------------
