
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm
from blog.models import Paste


def login(request):
    return render(request, 'registration/login.html')


def logout(request):
    return render(request, 'registration/login.html')


def signup(request):
    return render(request, 'registration/signup.html')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")
    template_name = "registration/login.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return super().form_valid(form)


def posts_list(request):
    user = request.user
    posts = Paste.objects.filter(author=user).order_by('-created_at')
    popular_posts = Paste.objects.order_by('-views_count')[:5]

    return render(request, 'users/users_posts.html', {
        'posts': posts,
        'popular_posts': popular_posts
    })

