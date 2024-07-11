import os
import smtplib
from email.mime.text import MIMEText
import unittest
from unittest.mock import patch, MagicMock
from accounts.utils import EmailSender


class TestEmailSender(unittest.TestCase):
    """유닛테스트 목업을 사용하여 진행"""

    def setUp(self):
        self.email_sender = EmailSender()
        self.recieve_email = "receiver@example.com"
        self.contents = "This is a test message."

    @patch("accounts.utils.smtplib.SMTP_SSL")
    def test_smtp_setting(self, mock_smtp_ssl):
        mock_smtp = MagicMock()
        mock_smtp_ssl.return_value = mock_smtp

        session = self.email_sender.smtp_setting()

        mock_smtp_ssl.assert_called_once_with(
            os.getenv("SMTP_SERVER_URL"), os.getenv("SMTP_SERVER_PORT")
        )
        mock_smtp.login.assert_called_once_with(
            os.getenv("SMTP_LOGIN_ID"), os.getenv("SMTP_LOGIN_PASSWORD")
        )

        self.assertEqual(session, mock_smtp)

    def test_email_data(self):
        email = self.recieve_email
        contents = self.contents
        msg = self.email_sender.email_data(email, contents)

        self.assertIsInstance(msg, MIMEText)
        self.assertEqual(
            msg["Subject"], "THE LONG DARK SUPPORT 페이지에서 발신된 메세지 입니다."
        )
        self.assertEqual(msg["From"], os.getenv("EMAIL_ADDRESS"))
        self.assertEqual(msg["To"], email)
        self.assertEqual(msg.get_payload(), contents)

    @patch("accounts.utils.EmailSender.smtp_setting")
    @patch("accounts.utils.EmailSender.email_data")
    @patch("accounts.utils.smtplib.SMTP_SSL")
    def test_send(self, mock_smtp_ssl, mock_email_data, mock_smtp_setting):
        mock_smtp = MagicMock()
        mock_smtp_ssl.return_value = mock_smtp
        mock_email_data.return_value = MIMEText(self.contents)
        mock_smtp_setting.return_value = mock_smtp

        self.email_sender.send(self.recieve_email, self.contents)

        mock_smtp.sendmail.assert_called_once_with(
            os.getenv("EMAIL_ADDRESS"),
            self.recieve_email,
            mock_email_data.return_value.as_string(),
        )
        mock_smtp.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
