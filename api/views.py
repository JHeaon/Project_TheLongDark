from django.shortcuts import render


def home(request):
    return render(request, "api/home.html")


def introduce(request):
    return render(request, "api/introduce.html")


def news(request, pk=None):
    if pk:
        return render(request, "api/news_detail.html")

    return render(request, "api/news.html")


def support(request):
    return render(request, "api/support.html")


def news_write(request):
    return render(request, "api/news_write.html")


def detail(request):
    return render(request, "api/detail.html")


def login(request):
    return render(request, "api/login.html")


def community(request, pk=None):
    if pk:
        return render(request, "api/community_detail.html")
    return render(request, "api/community.html")


def community_write(request):
    return render(request, "api/community_write.html")


def user(request):
    return render(request, "api/user.html")


def signup(request):
    return render(request, "api/signup.html")
