from django.contrib import admin

from .models import LikeDislikePaste, LikeDislikeComment

admin.site.register(LikeDislikePaste)
admin.site.register(LikeDislikeComment)
