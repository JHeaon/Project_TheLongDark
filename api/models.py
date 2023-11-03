from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to='image/')  # blank=True는 필수가 아님을 의미
    created_at = models.DateTimeField(auto_now_add=True)  # 자동으로 현재 시간을 넣어줌
    updated_at = models.DateTimeField(auto_now=True)  # 자동으로 현재 시간을 넣어줌

    def __str__(self):
        return self.title
