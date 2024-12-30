from django.urls import path

from tracker_app.views.dashboard import UserDashboardView
from tracker_app.views.landing import HeroSectionView
from tracker_app.views.login_register import UserLoginView, UserRegisterView

urlpatterns = [
    path("user_register/", UserRegisterView.as_view(), name="user_register"),
    path("login/", UserLoginView.as_view(), name="login"),
    # path("filter/", FilterFormView.as_view(), name="filter"),
    path("home/", UserDashboardView.as_view(), name="home"),
    path("", HeroSectionView.as_view(), name="hero"),
]
