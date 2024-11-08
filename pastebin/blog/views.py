from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PasteForm

from .backends.general_backends import add_tags_to_paste, verify_password, \
    process_time, handle_password, sort_and_filter
from .backends.post_logic_backends import handle_post_deletion, render_post_response, get_post_context

from .models import Paste, Comment, Category
from general.models import Notifications, Messages

from general.backends.general_backends import create_notification, create_message


# ----------------------------------------------------------------------------
# main page
def index(request):
    form = PasteForm()
    popular_posts = Paste.objects.order_by('-views_count')[:5]
    user = request.user
    context = {
        'form': form,
        'popular_posts': popular_posts,
    }
    if user.is_authenticated:
        unread_notifications_count = Notifications.objects.filter(user=request.user, is_checked=False).count()
        unread_messages_count = Messages.objects.filter(user=request.user, is_checked=False).count()
        context['unread_notifications_count'] = unread_notifications_count
        context['unread_messages_count'] = unread_messages_count

    return render(request, 'blog/index.html', context)


def posts_check(request):
    posts = Paste.objects.all()
    popular_posts = Paste.objects.order_by('-views_count')[:5]
    categories = Category.objects.all()

    category = request.GET.get('category')
    sort_by = request.GET.get('sort')
    access_status = request.GET.get('access_status')
    has_password = request.GET.get('has_password')
    search_query = request.GET.get('search', '')

    posts = sort_and_filter(posts, category, sort_by, access_status, has_password, search_query)

    return render(request, 'blog/posts.html', {
        'posts': posts,
        'popular_posts': popular_posts,
        'categories': categories,
        'selected_category': category,
        'selected_sort': sort_by,
        'has_password': has_password,
        'search_query': search_query
    })


# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# tags
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# comments

def create_comment(request, slug):
    post, popular_posts = get_post_context(request, slug)
    if request.method == "POST":
        comment = Comment.objects.create(
            author=request.user,
            paste=get_object_or_404(Paste, slug=slug),
            content=request.POST.get('content')
        )
        comment.save()
        create_notification(request, post, flag='comment')
        create_message(request, post, comment)
    return render_post_response(request, post, popular_posts, requires_password=False)


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

            paste.time_live = process_time(form)

            handle_password(form, paste, paste.password)

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
        post.delete()
        return redirect('users:posts-list')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def edit_post(request, slug):
    post, popular_posts = get_post_context(request, slug)

    old_hashed_password = post.password

    if request.method == 'POST':
        form = PasteForm(request.POST, instance=post)
        if form.is_valid():
            paste = form.save(commit=False)

            paste.time_live = process_time(form)
            password_error = handle_password(form, paste, old_hashed_password)

            if password_error:
                return render_post_response(request, post, popular_posts, requires_password=False,
                                            error_message="Пожалуйста, введите пароль или отключите его.")

            paste.save()
            add_tags_to_paste(paste, form.cleaned_data['tags'])

            return render_post_response(request, post, popular_posts, requires_password=False)
    else:
        form = PasteForm(instance=post)

    return render(request, 'post.html', {
        'form': form, 'post': post,
        'popular_posts': popular_posts,
    })


def detail_post(request, slug):
    post, popular_posts = get_post_context(request, slug)

    requires_password = bool(post.password)

    if requires_password and request.method == 'GET':
        return render_post_response(request, post, popular_posts, requires_password)

    if request.method == 'GET' and not requires_password:
        return handle_post_deletion(request, post, popular_posts)

    return render_post_response(request, post, popular_posts, requires_password)


def post_password_check(request, slug):
    post, popular_posts = get_post_context(request, slug)

    if request.method == 'POST':
        entered_password = request.POST.get('password')

        if verify_password(post.password, entered_password):
            post.save()
            return handle_post_deletion(request, post, popular_posts)

        return render_post_response(request, post, popular_posts, True,
                                    "Неверный пароль. Пожалуйста, попробуйте снова.")

    return redirect('blog:post-detail', slug=slug)

# ----------------------------------------------------------------------------
