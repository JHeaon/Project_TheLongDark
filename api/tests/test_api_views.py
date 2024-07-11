from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from api.models import NewsPost, NewsComment, CommunityPost, CommunityComment
from django.core.files.uploadedfile import SimpleUploadedFile
from api.forms import (
    NewsPostForm,
    NewsCommentForm,
    CommunityPostForm,
    CommunityCommentForm,
)

from PIL import Image
import io

User = get_user_model()


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@example.com", password="password123", is_staff=True
        )

        # TODO : 추후 user staff가 아닐때 포스트 요청 테스트 코드 작성하기
        self.user.is_staff = True

        self.client.login(email="test@example.com", password="password123")

        self.news_post = NewsPost.objects.create(
            user=self.user,
            title="Test News Post",
            contents="Test Contents",
            image=SimpleUploadedFile(
                name="test_image.jpg", content=b"", content_type="image/jpeg"
            ),
        )
        self.community_post = CommunityPost.objects.create(
            user=self.user, title="Test Community Post", contents="Test Contents"
        )

    def test_home_view(self):
        response = self.client.get(reverse("api:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/home.html")

    def test_introduce_view(self):
        response = self.client.get(reverse("api:introduce"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/introduce.html")

    def test_news_view(self):
        response = self.client.get(reverse("api:news"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/news.html")
        self.assertIn("news_list", response.context)
        self.assertIn("page_obj", response.context)

    def test_news_create_view_get(self):
        response = self.client.get(reverse("api:news_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/news_write.html")

    def test_news_create_view_post(self):
        image = Image.new("RGB", (100, 100), color="red")
        image_io = io.BytesIO()
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=image_io.read(),
            content_type="image/jpeg",
        )

        response = self.client.post(
            reverse("api:news_create"),
            {"title": "New News Post", "contents": "New contents", "image": image},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(NewsPost.objects.filter(title="New News Post").exists())

    def test_news_detail_view(self):
        response = self.client.get(reverse("api:news_detail", args=[self.news_post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/news_detail.html")
        self.assertIn("news", response.context)
        self.assertIn("comments", response.context)

    def test_news_update_view_get(self):
        response = self.client.get(reverse("api:news_update", args=[self.news_post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/news_write.html")
        self.assertIn("news_post", response.context)

    def test_news_update_view_post(self):
        response = self.client.post(
            reverse("api:news_update", args=[self.news_post.id]),
            {"title": "Updated News Post", "contents": "Updated contents"},
        )
        self.assertEqual(response.status_code, 302)
        self.news_post.refresh_from_db()
        self.assertEqual(self.news_post.title, "Updated News Post")

    def test_news_delete_view(self):
        response = self.client.get(reverse("api:news_delete", args=[self.news_post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(NewsPost.objects.filter(id=self.news_post.id).exists())

    def test_news_comment_create_view(self):
        response = self.client.post(
            reverse("api:news_comment_create", args=[self.news_post.id]),
            {"contents": "New comment"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(NewsComment.objects.filter(contents="New comment").exists())

    def test_community_view(self):
        response = self.client.get(reverse("api:community"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/community.html")
        self.assertIn("community_posts", response.context)

    def test_community_detail_view(self):
        response = self.client.get(
            reverse("api:community_detail", args=[self.community_post.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/community_detail.html")
        self.assertIn("community_post", response.context)
        self.assertIn("community_comments", response.context)

    def test_community_create_view_get(self):
        response = self.client.get(reverse("api:community_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/community_write.html")

    def test_community_create_view_post(self):
        response = self.client.post(
            reverse("api:community_create"),
            {"title": "New Community Post", "contents": "New contents"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            CommunityPost.objects.filter(title="New Community Post").exists()
        )

    def test_community_update_view_get(self):
        response = self.client.get(
            reverse("api:community_update", args=[self.community_post.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/community_write.html")
        self.assertIn("community_post", response.context)

    def test_community_update_view_post(self):
        response = self.client.post(
            reverse("api:community_update", args=[self.community_post.id]),
            {"title": "Updated Community Post", "contents": "Updated contents"},
        )
        self.assertEqual(response.status_code, 302)
        self.community_post.refresh_from_db()
        self.assertEqual(self.community_post.title, "Updated Community Post")

    def test_community_delete_view(self):
        response = self.client.get(
            reverse("api:community_delete", args=[self.community_post.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            CommunityPost.objects.filter(id=self.community_post.id).exists()
        )

    def test_community_comment_create_view(self):
        response = self.client.post(
            reverse("api:community_comment_create", args=[self.community_post.id]),
            {"contents": "New comment"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            CommunityComment.objects.filter(contents="New comment").exists()
        )
