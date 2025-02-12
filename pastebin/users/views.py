from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from .backends.users_backends import sort_and_filter, create_random_pastes
from .forms import CustomUserCreationForm
from blog.models import Paste

from general.models import Notifications
from general.backends.general_backends import create_notification

from blog.models import Category


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


@login_required
def posts_list(request):
    user = request.user
    posts = Paste.objects.filter(author=user).order_by('-created_at')
    popular_posts = Paste.objects.order_by('-views_count')[:5]

    categories = Category.objects.all()

    category = request.GET.get('category')
    sort_by = request.GET.get('sort')
    access_status = request.GET.get('access_status')
    has_password = request.GET.get('has_password')
    search_query = request.GET.get('search', '')

    try:
        posts = sort_and_filter(posts, category, sort_by, access_status, has_password, search_query)
    except Exception as e:
        print(f'Произошла ошибка во время сортировки и фильтрации: {e}')

    return render(request, 'users_posts.html', {
        'posts': posts,
        'popular_posts': popular_posts,
        'categories': categories,
        'selected_category': category,
        'selected_sort': sort_by,
        'has_password': has_password,
        'search_query': search_query
    })


@csrf_exempt
@login_required
def toggle_favorite(request, slug):
    post = get_object_or_404(Paste, slug=slug)
    user = request.user

    notifications = Notifications.objects.filter(sender=user, post=post, notification_type=Notifications.FAVOURITE)

    if not notifications:
        create_notification(request, post, flag='favourite')

    if post in user.favorites.all():
        user.favorites.remove(post)
        is_favorite = False
        if post.favourite_count > 0:
            post.favourite_count = post.favourite_count - 1
    else:
        user.favorites.add(post)
        is_favorite = True
        post.favourite_count = post.favourite_count + 1
    post.save()

    return JsonResponse({'is_favorite': is_favorite})


def profile(request):
    popular_posts = Paste.objects.order_by('-views_count')[:5]
    return render(request, 'user_profile.html', {
        'popular_posts': popular_posts,
    })


@login_required
def update_profile(request):
    popular_posts = Paste.objects.order_by('-views_count')[:5]
    user = request.user

    try:
        create_random_pastes(user, 100)
    except Exception as e:
        print(f'Произошла ошибка во время генерации случайных постов: {e}')

    if request.method == 'POST':
        username = request.POST.get('username', user.username)
        email = request.POST.get('email', user.email)
        bio = request.POST.get('bio', user.bio)
        address = request.POST.get('address', user.address)

        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        user.username = username
        user.email = email
        user.bio = bio
        user.address = address

        user.save()

        return redirect('users:user-profile')

    return render(request, 'user_profile.html', {
        'user': user,
        'popular_posts': popular_posts
    })


@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change_page.html'
    success_url = reverse_lazy('users:password-change-done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Paste.objects.order_by('-views_count')[:5]
        return context


@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'password_change_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Paste.objects.order_by('-views_count')[:5]
        return context


def subscription(request):
    popular_posts = Paste.objects.order_by('-views_count')[:5]
    return render(request, 'subscription.html', {
        'popular_posts': popular_posts
    })
