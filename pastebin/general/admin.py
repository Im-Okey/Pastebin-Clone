from django.contrib import admin

from .models import LikeDislikePaste, LikeDislikeComment, Notifications, Messages

admin.site.register(LikeDislikePaste)
admin.site.register(LikeDislikeComment)
admin.site.register(Notifications)
admin.site.register(Messages)
