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
    if request.method == "POST":

        # Post 요청이 들어오면 내 이메일로 문의 내역이 전송되어야 한다.
        pass

    return render(request, "api/support.html")

def detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, "api/detail.html", {"post": post})