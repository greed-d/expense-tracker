from django.urls import path

from tracker_app import views

urlpatterns = [
    path("user_register/", views.UserRegisterView.as_view(), name="user_register"),
    path("login/", views.UserLoginStuff.as_view(), name="login"),
    path("home/", views.UserDashboardView.as_view(), name="home"),
    path("", views.HeroSectionView.as_view(), name="hero"),
]
