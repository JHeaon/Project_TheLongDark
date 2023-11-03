from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "api/home.html")

def introduce(request):
    return render(request, "api/introduce.html")

def news(request):
    return render(request, "api/news.html")

def support(request):
    return render(request, "api/support.html")