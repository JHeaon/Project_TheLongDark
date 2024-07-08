from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("", views.home, name="home"),
    path("introduce/", views.introduce, name="introduce"),
    path("news/", views.news, name="news"),
    path("news/<int:pk>", views.news, name="news_detail"),
    path("news_write/", views.news_write, name="news_write"),
    path("community/", views.community, name="community"),
    path("community/<int:pk>", views.community, name="community_detail"),
    path("community_write/", views.community_write, name="community_write"),
    path("support/", views.support, name="support"),
    path("login/", views.login, name="login"),
    path("user/", views.user, name="user"),
    path("signup/", views.signup, name="signup"),
]
