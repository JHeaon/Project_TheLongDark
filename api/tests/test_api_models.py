from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import TimeStampedModel
from api.models import (
    CommunityPost,
    CommunityComment,
    NewsPost,
    NewsComment,
    SupportPost,
)
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class ModelsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="password123"
        )
        self.community_post = CommunityPost.objects.create(
            user=self.user,
            title="Community Post Title",
            contents="Community Post Contents",
        )
        self.news_post = NewsPost.objects.create(
            user=self.user,
            title="News Post Title",
            contents="News Post Contents",
            image=SimpleUploadedFile(
                name="test_image.jpg", content=b"", content_type="image/jpeg"
            ),
        )

    def test_community_post_creation(self):
        """커뮤니티 글 생성"""
        post = CommunityPost.objects.create(
            user=self.user, title="Another Community Post", contents="More Contents"
        )
        self.assertEqual(str(post), post.title)
        self.assertEqual(post.user.email, "test@example.com")

    def test_community_comment_creation(self):
        """커뮤니티 댓글 생성"""
        comment = CommunityComment.objects.create(
            user=self.user, community_post=self.community_post, contents="A comment"
        )
        self.assertEqual(
            str(comment), f"Comment by {self.user.email} on {self.community_post.title}"
        )
        self.assertEqual(comment.community_post.title, "Community Post Title")

    def test_news_post_creation(self):
        """뉴스 글 생성"""
        self.assertEqual(str(self.news_post), self.news_post.title)
        self.assertEqual(self.news_post.user.email, "test@example.com")

    def test_news_comment_creation(self):
        """뉴스 댓글 생성"""
        comment = NewsComment.objects.create(
            user=self.user, news_post=self.news_post, contents="News comment"
        )
        self.assertEqual(str(comment), self.news_post.title)
        self.assertEqual(comment.news_post.title, "News Post Title")

    def test_support_post_creation(self):
        """지원글 생성"""
        support_post = SupportPost.objects.create(
            name="Supporter", email="support@example.com", contents="Help needed"
        )
        self.assertEqual(str(support_post), "Support Post by Supporter")
        self.assertEqual(support_post.email, "support@example.com")
