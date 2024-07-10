from django import forms
from api.models import *


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ["title", "contents", "image"]
