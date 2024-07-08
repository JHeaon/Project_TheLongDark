from django.shortcuts import render, redirect, reverse
from django.db import IntegrityError
from django.views import View
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    get_user_model,
    logout as auth_logout,
)


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


class login(View):
    template_name = "api/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user_data = {
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
        }

        user = authenticate(**user_data)
        print(user)

        if user:
            auth_login(request, user)
            return redirect(reverse("api:home"))

        return render(
            request,
            self.template_name,
            {"error": "유효하지 않은 이메일 혹은 비밀번호 입니다."},
        )


def community(request, pk=None):
    if pk:
        return render(request, "api/community_detail.html")
    return render(request, "api/community.html")


def community_write(request):
    return render(request, "api/community_write.html")


def user(request):
    return render(request, "api/user.html")


class signup(View):
    template_name = "api/signup.html"

    def get(self, reqeust):
        return render(reqeust, self.template_name)

    def post(self, request):

        user_data = {
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
            "name": request.POST.get("name"),
        }

        try:
            user = get_user_model().objects.create_user(**user_data)
        except IntegrityError:
            return render(
                request, self.template_name, {"error": "이미 존재하는 이메일 입니다. "}
            )

        return redirect(reverse("api:home"))


class logout(View):
    def get(self, request):
        auth_logout(request)
        return redirect(reverse("api:home"))


class user_update(View):
    template_name = "api/user_update.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.user
        user.introduce = request.POST.get("introduce")

        if "image" in request.FILES:
            user.image = request.FILES.get("image")

        user.save()

        return redirect(reverse("api:user"))
