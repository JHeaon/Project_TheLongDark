from django.contrib import admin
from api.models import (
    CommunityPost,
    CommunityComment,
    NewsPost,
    NewsComment,
    SupportPost,
)


@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "create_at")
    search_fields = ("title", "contents")
    list_filter = ("create_at", "user")


@admin.register(CommunityComment)
class CommunityCommentAdmin(admin.ModelAdmin):
    list_display = ("community_post", "user", "create_at")
    search_fields = ("contents", "community_post__title")
    list_filter = ("create_at", "user")


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "create_at")
    search_fields = ("title", "contents")
    list_filter = ("create_at", "user")


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ("news_post", "user", "create_at")
    search_fields = ("contents", "news_post__title")
    list_filter = ("create_at", "user")


@admin.register(SupportPost)
class SupportPostAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "create_at")
    search_fields = ("name", "email", "contents")
    list_filter = ("create_at",)
