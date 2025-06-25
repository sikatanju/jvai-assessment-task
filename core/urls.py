from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.user_register),
    path('profile/', views.user_profile),
    path('activate/', views.user_activate),
]
