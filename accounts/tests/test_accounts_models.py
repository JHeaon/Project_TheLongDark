from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


class UserModelTests(TestCase):

    def setUp(self):
        self.User = get_user_model()

    def test_create_user_with_email_successful(self):
        """유저 생성"""
        email = "test@example.com"
        password = "Testpass123"
        user = self.User.objects.create_user(
            email=email, password=password, name="Test User"
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.name, "Test User")

    def test_new_user_email_normalized(self):
        """유저 이메일 정규화 체크"""
        email = "test@EXAMPLE.COM"
        user = self.User.objects.create_user(email, "test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """이메일 없이 유저 생성시 에러"""
        with self.assertRaises(ValueError):
            self.User.objects.create_user(None, "test123")

    def test_create_new_superuser(self):
        """슈퍼유저 생성"""
        email = "superuser@example.com"
        password = "Superpass123"
        user = self.User.objects.create_superuser(email=email, password=password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_duplicate_email_error(self):
        """이메일 중복 유저 생성 에러"""
        email = "test@example.com"
        self.User.objects.create_user(email=email, password="test123")
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(email=email, password="test123")

    def test_user_str(self):
        """유저 객체 이름과 유저 이메일 비교"""
        user = self.User.objects.create_user(
            email="test@example.com", password="test123", name="Test User"
        )

        self.assertEqual(str(user), user.email)
