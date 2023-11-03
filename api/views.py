from django.shortcuts import render
from .models import Post

# Create your views here.
def home(request):
    return render(request, "api/home.html")

def introduce(request):
    return render(request, "api/introduce.html")

def news(request):
    posts = Post.objects.filter().order_by('-created_at')
    return render(request, "api/news.html", {"posts": posts})

def support(request):
    return render(request, "api/support.html")

def detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, "api/detail.html", {"post": post})