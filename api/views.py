import os

from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View

from api.models import *
from api.forms import *


def home(request):
    return render(request, "api/home.html")


def introduce(request):
    return render(request, "api/introduce.html")


class News(View):
    template_name = "api/news.html"

    def get(self, request, pk=None) -> HttpResponse:
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
        return render(request, "401.html")

    def post(self, request):
        if request.user.is_staff:
            form = NewsPostForm(request.POST, request.FILES)
            if form.is_valid():
                news_post = form.save(commit=False)
                news_post.user = request.user
                news_post.save()
                return redirect(reverse("api:news"))
        return render(request, "400.html")


class NewsDetail(View):
    def get(self, request, pk):
        news = NewsPost.objects.select_related("user").get(pk=pk)
        comments = news.newscomment_set.select_related("user").filter(news_post=news)
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
            form = NewsPostForm(request.POST, request.FILES, instance=news_post)
            if form.is_valid():
                form.save()
                return redirect(reverse("api:news"))

        return render(request, "404.html")


class NewsDelete(View):
    def get(self, request, pk):
        if request.user.is_staff:
            news_post = NewsPost.objects.get(pk=pk)
            news_post.delete()
            return redirect(reverse("api:news"))
        return render(request, "404.html")


class NewsCommentCreate(View):
    def post(self, request, pk=None):
        if request.user.is_authenticated:
            form = NewsCommentForm(request.POST)
            if form.is_valid():
                news_comment = form.save(commit=False)
                news_comment.news_post = NewsPost.objects.get(pk=pk)
                news_comment.user = request.user
                news_comment.save()
                return redirect(reverse("api:news_detail", args=(pk,)))

        return render(request, "401.html")


class Community(View):
    template_name = "api/community.html"

    def get(self, request, pk=None):
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


class CommunityDetail(View):
    def get(self, request, pk):
        community_post = CommunityPost.objects.select_related("user").get(pk=pk)
        community_comments = CommunityComment.objects.select_related("user").filter(
            community_post=pk
        )
        context = {
            "community_post": community_post,
            "community_comments": community_comments,
        }
        return render(request, "api/community_detail.html", context=context)


class CommunityCreate(View):
    template_name = "api/community_write.html"

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        return render(request, "401.html")

    def post(self, request):
        if request.user.is_authenticated:
            form = CommunityPostForm(request.POST)
            if form.is_valid():
                community_post = form.save(commit=False)
                community_post.user = request.user
                community_post.save()
                return redirect(reverse("api:community"))
        return render(request, "400.html")


class CommunityUpdate(View):
    def get(self, request, pk):
        community_post = CommunityPost.objects.get(pk=pk)
        if community_post.user == request.user:
            context = {"community_post": community_post}
            return render(request, "api/community_write.html", context=context)
        return render(request, "404.html")

    def post(self, request, pk):
        community_post = CommunityPost.objects.get(pk=pk)
        if community_post.user == request.user:
            form = CommunityPostForm(request.POST, instance=community_post)
            if form.is_valid():
                form.save()
                return redirect(reverse("api:community_detail", args=(pk,)))

        return render(request, "400.html")


class CommunityDelete(View):
    def get(self, request, pk):
        community_post = CommunityPost.objects.get(pk=pk)
        if request.user.is_staff or community_post.user == request.user:
            community_post.delete()
            return redirect(reverse("api:community"))

        return render(request, "404.html")


class CommunityCommentCreate(View):
    def post(self, request, pk=None):
        community_post = CommunityPost.objects.get(pk=pk)
        CommunityComment.objects.create(
            user=request.user,
            community_post=community_post,
            contents=request.POST.get("contents"),
        )
        return redirect(reverse("api:community_detail", args=(pk,)))
