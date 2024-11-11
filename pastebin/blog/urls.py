from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # main page
    path('', views.index, name='index'),
    path('posts_check/', views.posts_check, name='posts-check'),

    # # tags logic
    # path('tags/create/', views.TagCreateView.as_view(), name='tag-create'),
    # path('tags/update/<int:pk>/', views.TagUpdateView.as_view(), name='tag-update'),
    # path('tags/delete/<int:pk>/', views.TagDeleteView.as_view(), name='tag-delete'),

    # path('categories/', views.CategoryListView.as_view(), name='category-list'),
    # path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    # path('categories/update/<int:id>', views.CategoryUpdateView.as_view(), name='category-update'),
    # path('categories/delete/<int:id>', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('comments/create/<slug:slug>', views.create_comment, name='comment-create'),

    path('posts/create/', views.create_paste, name='create-paste'),
    path('posts/<slug:slug>/', views.detail_post, name='post-detail'),
    path('posts/update/<slug:slug>', views.edit_post, name='post-update'),
    path('posts/delete/<int:pk>', views.delete_paste, name='post-delete'),
    path('posts/<slug:slug>/check-password/', views.post_password_check, name='post-password-check'),

]
