from django.contrib import admin
from django.urls import path

from tracker_app import views

urlpatterns = [
    path("user_register/", views.UserRegisterView.as_view(), name="user_register"),
    path("", views.UserLoginStuff.as_view(), name="login"),
    path("home/", views.UserDashboardView.as_view(), name="home"),
]
