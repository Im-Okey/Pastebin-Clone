from django.contrib import admin

from .models import TagSubscription, UserFollow

admin.site.register(TagSubscription)
admin.site.register(UserFollow)
