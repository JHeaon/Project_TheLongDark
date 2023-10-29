from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "api/home.html")

def gameplay(request):
    return render(request, "api/gameplay.html")

def community(request):
    return render(request, "api/community.html")

def support(request):
    return render(request, "api/support.html")