from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    # 접속 페이지
    path("", views.home, name="home"),
    # 뉴스 페이지
    path("introduce/", views.introduce, name="introduce"),
    path("news/", views.news, name="news"),
    path("news/<int:pk>", views.news, name="news_detail"),
    path("news_write/", views.news_write, name="news_write"),
    # 커뮤니티 페이지
    path("community/", views.community, name="community"),
    path("community/<int:pk>", views.community, name="community_detail"),
    path("community_write/", views.community_write, name="community_write"),
    # 유저 페이지
    path("support/", views.support, name="support"),
    path("login/", views.login.as_view(), name="login"),
    path("logout/", views.logout.as_view(), name="logout"),
    path("signup/", views.signup.as_view(), name="signup"),
    path("user/", views.user, name="user"),
]
