from django.contrib.auth import get_user_model
from django.test import TestCase
from api.forms import (
    NewsPostForm,
    NewsCommentForm,
    CommunityPostForm,
    CommunityCommentForm,
)
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

User = get_user_model()


class FormsTestCase(TestCase):
    def test_news_post_form_valid(self):
        form_data = {"title": "Test News Post", "contents": "Test contents"}

        image = Image.new("RGB", (100, 100), color="red")
        image_io = io.BytesIO()
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        file_data = {
            "image": SimpleUploadedFile(
                name="test_image.jpg",
                content=image_io.read(),
                content_type="image/jpeg",
            )
        }

        form = NewsPostForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_news_post_form_invalid(self):
        """제목 없을시 에러"""
        form_data = {"title": "", "contents": "Test contents"}
        form = NewsPostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_news_comment_form_valid(self):
        form_data = {"contents": "Test comment"}
        form = NewsCommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_news_comment_form_invalid(self):
        """내용이 없으면 에러"""
        form_data = {"contents": ""}
        form = NewsCommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("contents", form.errors)

    def test_community_post_form_valid(self):
        form_data = {"title": "Test Community Post", "contents": "Test contents"}
        form = CommunityPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_community_post_form_invalid(self):
        form_data = {"title": "", "contents": "Test contents"}
        form = CommunityPostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_community_comment_form_valid(self):
        form_data = {"contents": "Test comment"}
        form = CommunityCommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_community_comment_form_invalid(self):
        """내용이 없으면 에러"""
        form_data = {"contents": ""}
        form = CommunityCommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("contents", form.errors)
