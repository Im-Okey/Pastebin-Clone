from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from .forms import CustomUserCreationForm
from blog.models import Paste


def login(request):
    return render(request, 'users/registration/login.html')


def logout(request):
    return render(request, 'users/registration/login.html')


def signup(request):
    return render(request, 'users/registration/signup.html')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")
    template_name = "users/registration/login.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return super().form_valid(form)


@login_required
def posts_list(request):
    user = request.user
    posts = Paste.objects.filter(author=user).order_by('-created_at')
    popular_posts = Paste.objects.order_by('-views_count')[:5]

    return render(request, 'users/users_posts.html', {
        'posts': posts,
        'popular_posts': popular_posts
    })


@csrf_exempt
@login_required
def toggle_favorite(request, slug):
    post = get_object_or_404(Paste, slug=slug)
    user = request.user

    if post in user.favorites.all():
        user.favorites.remove(post)
        is_favorite = False
    else:
        user.favorites.add(post)
        is_favorite = True

    return JsonResponse({'is_favorite': is_favorite})
