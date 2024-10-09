
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('register/', views.signup, name='register'),

    path('posts/', views.posts_list, name='posts-list'),
]
