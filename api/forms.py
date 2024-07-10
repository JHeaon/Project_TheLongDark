from django import forms
from api.models import *


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ["title", "contents", "image"]


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ["contents"]


class CommunityPostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ["title", "contents"]


class CommunityCommentForm(forms.ModelForm):
    class Meta:
        model = CommunityComment
        fields = ["contents"]
