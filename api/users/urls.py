from django.urls import path, include
from . import views

urlpatterns = [
    path('api/users/login', views.Authentication.as_view(), name='login'),
    path('api/users', views.Registration.as_view(), name='register'),
    path('api/user', views.AuthUser.as_view(), name='auth-user'),
    path('api/profiles/<str:username>', views.Profile.as_view(), name='profile'),

    path('api/profiles/<str:username>/follow', views.FollowingUser.as_view(), name='following'),
]
