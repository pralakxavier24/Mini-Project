# from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import index, login, user_Details, register

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('api-token-auth/', obtain_auth_token, name='obtain_auth_token'),
    path('blog/', user_Details.as_view(), name='blog'),
    path('blog/<int:id>', user_Details.as_view(), name='create'),
]