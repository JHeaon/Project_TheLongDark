from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(null=False, upload_to='image/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Request(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.EmailField()
    email = models.EmailField()
    context = models.TextField()

    def __str__(self):
        return self.email