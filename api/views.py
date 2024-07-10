import os

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    get_user_model,
    logout as auth_logout,
)

from api.models import *
from api.forms import *
from api import utils


def home(request):
    return render(request, "api/home.html")


def introduce(request):
    return render(request, "api/introduce.html")


class News(View):
    template_name = "api/news.html"

    def get(self, request, pk=None):
        news_list = NewsPost.objects.all().order_by("-id")
        paginator = Paginator(news_list, 3)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "news_list": news_list,
            "page_obj": page_obj,
        }
        return render(request, self.template_name, context=context)


class NewsCreate(View):
    template_name = "api/news_write.html"

    def get(self, request):
        if request.user.is_staff:
            return render(request, self.template_name)
        return render(request, "401.html", status=401)

    def post(self, request):
        if request.user.is_staff:
            form = NewsPostForm(request.POST, request.FILES)
            if form.is_valid():
                news_post = form.save(commit=False)
                news_post.user = request.user
                news_post.save()
                return redirect(reverse("api:news"))
        return render(request, "400.html", status=400)


class NewsDetail(View):
    def get(self, request, pk):
        news = NewsPost.objects.prefetch_related(
            "newscomment_set",
            "newscomment_set__user",
        ).get(pk=pk)
        comments = news.newscomment_set.all()
        context = {"news": news, "comments": comments}
        return render(request, "api/news_detail.html", context=context)


class NewsUpdate(View):
    def get(self, request, pk):
        if request.user.is_staff:
            news_post = NewsPost.objects.get(pk=pk)
            context = {"news_post": news_post}
            return render(request, "api/news_write.html", context=context)

    def post(self, request, pk):
        if request.user.is_staff:
            news_post = NewsPost.objects.get(pk=pk)
            print(request.POST)
            form = NewsPostForm(request.POST, request.FILES, instance=news_post)
            if form.is_valid():
                print(form.data)
                form.save()
                return redirect(reverse("api:news"))

        return render(request, "404.html")


class NewsDelete(View):
    def get(self, request, pk):
        news_post = get_object_or_404(NewsPost, pk=pk)

        if check_user(request, news_post):
            news_post.delete()
            return redirect(reverse("api:news"))

        return render(request, "404.html")


class NewsCommentCreate(View):
    def post(self, request, pk=None):
        news_post = NewsPost.objects.get(pk=pk)
        NewsComment.objects.create(
            user=request.user,
            news_post=news_post,
            contents=request.POST.get("contents"),
        )
        return redirect(reverse("api:news_detail", args=(pk,)))


class Support(View):
    def get(self, request):
        return render(request, "api/support.html")

    def post(self, request):
        name = request.POST.get("first_name") + request.POST.get("last_name")
        email = request.POST.get("email")
        contents = request.POST.get("contents")

        msg = f"""
        답신 이메일 : {email}
        성함 : {name}
        문의 내용 : {contents}
        """

        sender = utils.EmailSender()
        sender.send(os.getenv("EMAIL_ADDRESS"), msg)

        return redirect(reverse("api:home"))


def detail(request):
    return render(request, "api/detail.html")


class Login(View):
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


class Community(View):
    template_name = "api/community.html"

    def get(self, request, pk=None):
        if pk:
            community_post = CommunityPost.objects.get(pk=pk)
            community_comments = CommunityComment.objects.filter(community_post=pk)
            context = {
                "community_post": community_post,
                "community_comments": community_comments,
            }
            return render(request, "api/community_detail.html", context=context)

        community_posts = (
            CommunityPost.objects.select_related("user").all().order_by("-id")
        )
        paginator = Paginator(community_posts, 10)  # Show 10 posts per page.

        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {"community_posts": posts}
        return render(request, self.template_name, context=context)

    def post(self, request, pk=None):
        community_post = get_object_or_404(CommunityPost, pk=pk)
        CommunityComment.objects.create(
            user=request.user,
            community_post=community_post,
            contents=request.POST.get("contents"),
        )
        return redirect(reverse("api:community_detail", args=(pk,)))


class Community_write(View):
    template_name = "api/community_write.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        CommunityPost.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            contents=request.POST.get("contents"),
        )
        return redirect(reverse("api:community"))


def user(request):
    return render(request, "api/user.html")


class SignUp(View):
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


class Logout(View):
    def get(self, request):
        auth_logout(request)
        return redirect(reverse("api:home"))


class UserUpdate(View):
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


class CommunityUpdate(View):
    def get(self, request, pk):
        community_post = get_object_or_404(CommunityPost, pk=pk)

        if check_user(request, community_post):

            context = {"community_post": community_post}
            return render(request, "api/community_write.html", context=context)

        return render(request, "404.html")

    def post(self, request, pk):
        community_post = get_object_or_404(CommunityPost, pk=pk)
        if check_user(request, community_post):
            community_post.title = request.POST.get("title")
            community_post.contents = request.POST.get("contents")
            community_post.save()
            return redirect(reverse("api:community_detail", args=(pk,)))

        return render(request, "404.html")


class CommunityDelete(View):
    def get(self, request, pk):
        community_post = get_object_or_404(CommunityPost, pk=pk)

        if check_user(request, community_post):
            community_post.delete()
            return redirect(reverse("api:community"))

        return render(request, "404.html")


def check_user(request, queryset) -> bool:
    return request.user == queryset.user or request.user.is_staff
