from django.shortcuts import render, redirect, get_object_or_404

from .models import Notifications, Messages
from blog.models import Paste


def notifications(request):
    notes = Notifications.objects.all().filter(user=request.user)
    popular_posts = Paste.objects.order_by('-views_count')[:5]

    return render(request, 'notifications.html', {
        'popular_posts': popular_posts,
        'notes': notes,
    })


def messages(request):
    mess = Messages.objects.all().filter(user=request.user)
    unread_messages = mess.filter(is_checked=False)
    read_messages = mess.filter(is_checked=True)
    popular_posts = Paste.objects.order_by('-views_count')[:5]
    return render(request, 'messages.html', {
        'popular_posts': popular_posts,
        'messages': mess,
        'unread_messages': unread_messages,
        'read_messages': read_messages
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
