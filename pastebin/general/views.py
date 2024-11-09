from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .backends.general_backends import create_notification
from .models import Notifications, Messages, LikeDislikePaste
from blog.models import Paste


def notifications(request):
    notes = Notifications.objects.all().filter(user=request.user).order_by('-send_time')
    popular_posts = Paste.objects.order_by('-views_count')[:5]
    paginator = Paginator(notes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notifications.html', {
        'popular_posts': popular_posts,
        'notes': notes,
        'page_obj': page_obj,
    })


def messages(request):
    mess = Messages.objects.all().filter(user=request.user)

    unread_messages = mess.filter(is_checked=False)
    read_messages = mess.filter(is_checked=True)

    unread_paginator = Paginator(unread_messages, 4)  # 10 сообщений на страницу
    unread_page_number = request.GET.get('unread_page')
    unread_page_obj = unread_paginator.get_page(unread_page_number)

    read_paginator = Paginator(read_messages, 4)  # 10 сообщений на страницу
    read_page_number = request.GET.get('read_page')
    read_page_obj = read_paginator.get_page(read_page_number)

    popular_posts = Paste.objects.order_by('-views_count')[:5]

    return render(request, 'messages.html', {
        'popular_posts': popular_posts,
        'unread_messages': unread_page_obj,
        'read_messages': read_page_obj,
    })


def mark_all_read_notifications(request):
    Notifications.objects.filter(user=request.user, is_checked=False).update(is_checked=True)
    return redirect('general:notifications')


def mark_all_read_messages(request):
    Messages.objects.filter(user=request.user, is_checked=False).update(is_checked=True)
    return redirect('general:messages')


def mark_message_as_read(request, message_id):
    message = get_object_or_404(Messages, id=message_id)

    if not message.is_checked:
        message.is_checked = True
        message.save()

    return redirect('blog:post-detail', slug=message.post.slug)


def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notifications, id=notification_id)

    if not notification.is_checked:
        notification.is_checked = True
        notification.save()

    return redirect('blog:post-detail', slug=notification.post.slug)


@login_required
@csrf_exempt
def like_paste(request, paste_id):
    paste = Paste.objects.get(id=paste_id)
    user = request.user

    like_dislike_record = LikeDislikePaste.objects.filter(user=user, paste=paste).first()

    if like_dislike_record:
        if like_dislike_record.action == 1:
            like_dislike_record.delete()
            return JsonResponse({
                'likes_count': paste.likes_dislikes.filter(action=1).count(),
                'dislikes_count': paste.likes_dislikes.filter(action=-1).count(),
                'liked': False,
                'disliked': False,
            })
        else:
            like_dislike_record.action = 1
            like_dislike_record.save()
    else:
        LikeDislikePaste.objects.create(user=user, paste=paste, action=1)
        create_notification(request, paste, 'like')

    return JsonResponse({
        'likes_count': paste.likes_dislikes.filter(action=1).count(),
        'dislikes_count': paste.likes_dislikes.filter(action=-1).count(),
        'liked': True,
        'disliked': False,
    })


@login_required
@csrf_exempt
def dislike_paste(request, paste_id):
    paste = Paste.objects.get(id=paste_id)
    user = request.user

    like_dislike_record = LikeDislikePaste.objects.filter(user=user, paste=paste).first()

    if like_dislike_record:
        if like_dislike_record.action == -1:
            like_dislike_record.delete()
            return JsonResponse({
                'likes_count': paste.likes_dislikes.filter(action=1).count(),
                'dislikes_count': paste.likes_dislikes.filter(action=-1).count(),
                'liked': False,
                'disliked': False,
            })
        else:
            like_dislike_record.action = -1
            like_dislike_record.save()
    else:
        LikeDislikePaste.objects.create(user=user, paste=paste, action=-1)
        create_notification(request, paste, 'dislike')

    return JsonResponse({
        'likes_count': paste.likes_dislikes.filter(action=1).count(),
        'dislikes_count': paste.likes_dislikes.filter(action=-1).count(),
        'liked': False,
        'disliked': True,
    })


