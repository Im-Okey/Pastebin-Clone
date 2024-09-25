from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .forms import PasteForm

from .backends.paste_backends import process_time_live, add_tags_to_paste, hash_password
from .models import Paste


# ----------------------------------------------------------------------------
# main page
def index(request):
    form = PasteForm()
    return render(request, 'blog/index.html', {'form': form})


def post_check(request):
    return render(request, 'blog/post.html')


def posts_check(request):
    return render(request, 'blog/posts.html')


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
# ----------------------------------------------------------------------------
