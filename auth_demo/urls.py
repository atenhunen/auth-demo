"""auth_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/

"""

from django.urls import path, include
from django.contrib import admin

from auth_demo.api.views import (
    UserList, UserDetails, GroupList, RegisterUser, Activate)
from auth_demo.api.login import Login
from auth_demo.api.update_password import UpdatePassword

# Setup the URLs and include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', UserList.as_view()),
    path('users/<pk>/', UserDetails.as_view()),
    path('groups/', GroupList.as_view()),
    path('users/register', RegisterUser.as_view()),
    path('activate/<activation_token>/', Activate.as_view()),
    path('login/', Login.as_view()),
    path('update-password/', UpdatePassword.as_view())
]
