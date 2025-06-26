from rest_framework.authtoken.views import obtain_auth_token 
from django.urls import path

from . import views

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('register/', views.user_register),
    path('profile/', views.user_profile),
    path('activate/', views.user_activate),
]
