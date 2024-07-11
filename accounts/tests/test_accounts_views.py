from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile


class AccountViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email="test@example.com", password="Testpass123", name="Test User"
        )
        self.user.save()

    def test_user_view(self):
        """유저 페이지"""
        self.client.login(email="test@example.com", password="Testpass123")
        response = self.client.get(reverse("accounts:user"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/user.html")

    def test_user_update_get(self):
        """유저 데이터 업데이트 페이지"""
        self.client.login(email="test@example.com", password="Testpass123")
        response = self.client.get(reverse("accounts:user_update"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/user_update.html")

    def test_user_update_post(self):
        """유저 데이터 변경 성공시"""
        self.client.login(email="test@example.com", password="Testpass123")
        response = self.client.post(
            reverse("accounts:user_update"),
            {
                "introduce": "Updated introduction",
                "image": SimpleUploadedFile(
                    "image.jpg", b"file_content", content_type="image/jpeg"
                ),
            },
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.introduce, "Updated introduction")

    def test_support_get(self):
        """지원 페이지"""
        response = self.client.get(reverse("accounts:support"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/support.html")

    def test_support_post(self):
        """지원 페이지 요청 성공 시"""
        response = self.client.post(
            reverse("accounts:support"),
            {
                "first_name": "Test",
                "last_name": "User",
                "email": "testuser@example.com",
                "contents": "This is a test message",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_login_get(self):
        """로그인 페이지"""
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_post_success(self):
        """로그인 성공 했을 떄"""
        response = self.client.post(
            reverse("accounts:login"),
            {"email": "test@example.com", "password": "Testpass123"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("api:home"))

    def test_login_post_failure(self):
        """로그인 실패시"""
        response = self.client.post(
            reverse("accounts:login"),
            {"email": "test@example.com", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")
        self.assertContains(response, "유효하지 않은 이메일 혹은 비밀번호 입니다.")

    def test_logout(self):
        """로그아웃 처리시"""
        self.client.login(email="test@example.com", password="Testpass123")
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("api:home"))

    def test_signup_get(self):
        """회원 가입 페이지"""
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_signup_post_success(self):
        """회원가입 성공시"""
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "email": "newuser@example.com",
                "password": "Newpass123",
                "name": "New User",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("api:home"))
        new_user = self.User.objects.get(email="newuser@example.com")
        self.assertIsNotNone(new_user)

    def test_signup_post_failure(self):
        """회원가입 실패시"""
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "email": "test@example.com",
                "password": "Testpass123",
                "name": "Test User",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")
        self.assertContains(response, "이미 존재하는 이메일 입니다.")
