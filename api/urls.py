from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("", views.gameplay, name="gameplay"),
    path("", views.community, name="community"),
    path("", views.support, name="support"),
]
