from django.shortcuts import render, redirect
from .models import Post, Request
from .send_email import send_email


# Create your views here.
def home(request):
    return render(request, "api/home.html")


def introduce(request):
    return render(request, "api/introduce.html")


def news(request):
    posts = Post.objects.filter().order_by('-created_at')
    return render(request, "api/news.html", {"posts": posts})

def write(request):
    if request.method == "POST":
        title = request.POST.get("title")
        context = request.POST.get("context")
        image = request.FILES.get('image')
        print(title, context, image)

        Post.objects.create(
            title=title,
            content=context,
            image=image,
        )

        return redirect("api:news")

    else:
        return render(request, "api/write.html")


def support(request):
    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        context = request.POST.get("context")

        Request.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            context=context,
        )

        send_email(first_name + last_name, email, context)

        return render(request, "api/support.html")

    else:
        return render(request, "api/support.html")


def detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, "api/detail.html", {"post": post})
