from django.contrib import admin
from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("", views.home, name="home"),
    path("introduce/", views.introduce, name="introduce"),
    path("news/", views.news, name="news"),
    path("support/", views.support, name="support"),
    path("write/", views.write, name="write"),
    path("detail/<int:pk>/", views.detail, name="detail"),
]
