import os
import smtplib
from email.mime.text import MIMEText


class EmailSender(object):
    """
    해당 클래스는 사용전 .env 파일에서 Email 전송을 위한 환경 변수을 받아와서 사용합니다.

    EMAIL_ADDRESS : 자신의 이메일 혹은 자신이 보여지고자 하는 이메일 // 예)test@example.com
    SMTP_LOGIN_ID= smtp 로그인 아이디 // 예)test_id
    SMTP_LOGIN_PASSWORD= smtp 패스워드 // 예)test_password
    SMTP_SERVER_URL=smtp 서버 url 주소 // 예)smtp.test.com
    SMTP_SERVER_PORT=smtp 서버 포트 주소 // 예)777
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def send(self, recieve_email, contents):

        session = self.smtp_setting()
        msg = self.email_data(recieve_email, contents)

        session.sendmail(os.getenv("EMAIL_ADDRESS"), recieve_email, msg.as_string())
        session.close()

    def smtp_setting(self):
        smtp_id = os.getenv("SMTP_LOGIN_ID")
        smtp_password = os.getenv("SMTP_LOGIN_PASSWORD")

        smtpName = os.getenv("SMTP_SERVER_URL")
        smtpPort = os.getenv("SMTP_SERVER_PORT")

        session = smtplib.SMTP_SSL(smtpName, smtpPort)  # 메일 서버 연결
        session.login(smtp_id, smtp_password)  # 로그인

        return session

    def email_data(self, email, contents):
        contents = f"{contents}"

        msg = MIMEText(contents)
        msg["Subject"] = "THE LONG DARK SUPPORT 페이지에서 발신된 메세지 입니다."
        msg["From"] = os.getenv("EMAIL_ADDRESS")
        msg["To"] = email

        return msg
