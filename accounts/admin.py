from django.contrib import admin
from accounts.models import User, EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    pass
