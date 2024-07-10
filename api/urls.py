from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    # 접속 및 소개 페이지
    path("", views.home, name="home"),
    path("introduce/", views.introduce, name="introduce"),
    # 뉴스 페이지
    path("news/", views.News.as_view(), name="news"),
    path("news/create", views.NewsCreate.as_view(), name="news_create"),
    path("news/<int:pk>", views.NewsDetail.as_view(), name="news_detail"),
    path("news/<int:pk>/update", views.NewsUpdate.as_view(), name="news_update"),
    path("news/<int:pk>/delete", views.NewsDelete.as_view(), name="news_delete"),
    # 뉴스 댓글 생성
    path(
        "news_comment/<int:pk>/",
        views.NewsCommentCreate.as_view(),
        name="news_comment_create",
    ),
    # 커뮤니티 페이지
    path("community/", views.Community.as_view(), name="community"),
    path("community/<int:pk>", views.Community.as_view(), name="community_detail"),
    path("community_write/", views.Community_write.as_view(), name="community_write"),
    path(
        "community/<int:pk>/update",
        views.CommunityUpdate.as_view(),
        name="community_update",
    ),
    path(
        "community/<int:pk>/delete",
        views.CommunityDelete.as_view(),
        name="community_delete",
    ),
    # 유저 페이지
    path("support/", views.Support.as_view(), name="support"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("user/", views.user, name="user"),
    path("user_update/", views.UserUpdate.as_view(), name="user_update"),
]
