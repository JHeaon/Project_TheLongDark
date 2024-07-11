import os

from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
    get_user_model,
)
from django.db import IntegrityError

from accounts import utils
from api.models import SupportPost


def user(request):
    return render(request, "accounts/user.html")


class UserUpdate(View):
    template_name = "accounts/user_update.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.user
        user.introduce = request.POST.get("introduce")

        if "image" in request.FILES:
            user.image = request.FILES.get("image")

        user.save()

        return redirect(reverse("accounts:user"))


class Support(View):
    def get(self, request):
        return render(request, "accounts/support.html")

    def post(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        name = first_name + last_name
        email = request.POST.get("email")
        contents = request.POST.get("contents")

        support_post = SupportPost.objects.create(
            name=name, email=email, contents=contents
        )

        msg = f"""
        답신 이메일 : {email}
        성함 : {name}
        문의 내용 : {contents}
        """

        sender = utils.EmailSender()
        sender.send(os.getenv("EMAIL_ADDRESS"), msg)

        return redirect(reverse("api:home"))


class Login(View):
    template_name = "accounts/login.html"

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


class Logout(View):
    def get(self, request):
        auth_logout(request)
        return redirect(reverse("api:home"))


class SignUp(View):
    template_name = "accounts/signup.html"

    def get(self, reqeust):
        return render(reqeust, self.template_name)

    def post(self, request):

        user_data = {
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
            "name": request.POST.get("name"),
        }

        print(user_data)

        try:
            user = get_user_model().objects.create_user(**user_data)
        except IntegrityError:
            return render(
                request, self.template_name, {"error": "이미 존재하는 이메일 입니다. "}
            )

        return redirect(reverse("api:home"))
