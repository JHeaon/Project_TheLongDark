from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    # 접속 및 소개 페이지
    path("", views.home, name="home"),
    path("introduce/", views.introduce, name="introduce"),
    # 뉴스 페이지
    path("news/", views.News.as_view(), name="news"),
    path("news/create/", views.NewsCreate.as_view(), name="news_create"),
    path("news/<int:pk>/", views.NewsDetail.as_view(), name="news_detail"),
    path("news/<int:pk>/update/", views.NewsUpdate.as_view(), name="news_update"),
    path("news/<int:pk>/delete/", views.NewsDelete.as_view(), name="news_delete"),
    path(
        "news/<int:pk>/comments/",
        views.NewsCommentCreate.as_view(),
        name="news_comment_create",
    ),
    # 커뮤니티 페이지
    path("community/", views.Community.as_view(), name="community"),
    path(
        "community/<int:pk>/", views.CommunityDetail.as_view(), name="community_detail"
    ),
    path("community/create/", views.CommunityCreate.as_view(), name="community_create"),
    path(
        "community/<int:pk>/update/",
        views.CommunityUpdate.as_view(),
        name="community_update",
    ),
    path(
        "community/<int:pk>/delete/",
        views.CommunityDelete.as_view(),
        name="community_delete",
    ),
    path(
        "community/<int:pk>/comments/",
        views.CommunityCommentCreate.as_view(),
        name="community_comment_create",
    ),
]
