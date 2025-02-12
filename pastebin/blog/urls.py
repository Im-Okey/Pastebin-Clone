from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # main page
    path('', views.index, name='index'),
    path('posts_check/', views.posts_check, name='posts-list'),

    # comments
    path('comments/create/<slug:slug>', views.create_comment, name='comment-create'),

    # posts
    path('posts/create/', views.create_paste, name='create-paste'),
    path('posts/<slug:slug>/', views.detail_post, name='post-detail'),
    path('posts/update/<slug:slug>', views.edit_post, name='post-update'),
    path('posts/delete/<int:pk>', views.delete_paste, name='post-delete'),
    path('posts/<slug:slug>/check-password/', views.post_password_check, name='post-password-check'),

]
