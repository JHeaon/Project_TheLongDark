from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # 유저 페이지
    path("support/", views.Support.as_view(), name="support"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("user/", views.user, name="user"),
    path("user_update/", views.UserUpdate.as_view(), name="user_update"),
]
