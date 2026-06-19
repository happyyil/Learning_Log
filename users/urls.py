"""Defines URL patterns for users"""

from django.urls import path, include
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'users'
urlpatterns = [
    # Logout page.
    path('logged_out/', views.logged_out, name='logged_out'),
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
    # User's profile
    #path('profile/', views.profile, name='profile'),
]
