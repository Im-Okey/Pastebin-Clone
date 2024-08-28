from django.contrib import admin

from .models import Category, Comment, Paste, Tag

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Paste)
admin.site.register(Tag)

