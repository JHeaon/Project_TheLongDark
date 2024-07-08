from core.models import TimeStampedModel
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CommunityPost(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    contents = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CommunityComment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community_post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE)
    contents = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email} on {self.community_post.title}"


class NewsPost(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="news_images/")
    title = models.CharField(max_length=255)
    contents = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class NewsComment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news_post = models.ForeignKey(NewsPost, on_delete=models.CASCADE)
    contents = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email} on {self.news_post.title}"


class SupportPost(TimeStampedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contents = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Support Post by {self.name}"
