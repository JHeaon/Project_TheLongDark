from django.contrib import admin
from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("", views.home, name="home"),
    path("gameplay/", views.gameplay, name="gameplay"),
    path("community/", views.community, name="community"),
    path("support/", views.support, name="support"),
]
