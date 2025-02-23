from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [

    # reg & auth
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('register/', views.signup, name='register'),

    # posts
    path('posts/', views.posts_list, name='posts-list'),
    path('toggle-favorite/<slug:slug>/', views.toggle_favorite, name='toggle-favorite'),

    # profile
    path('profile/', views.profile, name='user-profile'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('subscription/', views.subscription, name='subs'),


    path('test_pastes/', views.test_pastes, name='test-pastes'),

    # profile settings
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password-change'),
    path('password-change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password-change-done'),
]
