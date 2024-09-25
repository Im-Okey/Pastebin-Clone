
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # main page
    path('', views.index, name='index'),
    path('post_check/', views.post_check, name='post-check'),
    path('posts_check/', views.posts_check, name='posts-check'),

    # # tags logic
    # path('tags/', views.TagListView.as_view(), name='tag-list'),
    # path('tags/create/', views.TagCreateView.as_view(), name='tag-create'),
    # path('tags/update/<int:pk>/', views.TagUpdateView.as_view(), name='tag-update'),
    # path('tags/delete/<int:pk>/', views.TagDeleteView.as_view(), name='tag-delete'),


    # path('categories/', views.CategoryListView.as_view(), name='category-list'),
    # path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    # path('categories/update/<int:id>', views.CategoryUpdateView.as_view(), name='category-update'),
    # path('categories/delete/<int:id>', views.CategoryDeleteView.as_view(), name='category-delete'),

    # path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    # path('comments/update/<int:id>', CommentUpdateView.as_view(), name='comment-update'),
    # path('comments/delete/<int:id>', CommentDeleteView.as_view(), name='comment-delete'),


    path('posts/create/', views.create_paste, name='create-paste'),
    # path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('posts/update/<int:pk>', PostUpdateView.as_view(), name='post-update'),
    path('posts/delete/<int:pk>', views.delete_paste, name='post-delete'),

]