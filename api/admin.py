from django.contrib import admin
from .models import Post, Request


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass
