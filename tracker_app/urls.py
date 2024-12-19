from django.contrib import admin
from django.urls import path

from tracker_app import views

urlpatterns = [
    path("user_login/", views.UserRegisterView.as_view(), name="user_login"),
    path("dashboard/", views.UserDashboardView.as_view(), name="dashboard"),
]
