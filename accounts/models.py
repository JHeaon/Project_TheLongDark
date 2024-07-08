from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth import get_user_model
from core.models import TimeStampedModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("email must have not blank")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    introduce = models.TextField(blank=True)
    image = models.ImageField(upload_to="user_images/", null=True)

    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class EmailVerification(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    key = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user.email}"
