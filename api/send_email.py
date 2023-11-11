import os
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

def send_email(name, email, context):
    sendEmail = os.getenv('SENDEMAIL')
    recvEmail = os.getenv('RECVEMAIL')
    password = os.getenv('PASSWORD')

    smtpName = "smtp.naver.com" #smtp 서버 주소
    smtpPort = os.getenv('SMTPPORT') #smtp 포트 번호

    context = "이름 : name\n\n" + "이메일 : email\n\n" + "내용 :" + context
    msg = MIMEText(context) #MIMEText(text , _charset = "utf8")

    msg['Subject'] = email
    msg['From'] = sendEmail
    msg['To'] = recvEmail

    s=smtplib.SMTP(smtpName , smtpPort) #메일 서버 연결
    s.starttls() #TLS 보안 처리
    s.login(sendEmail , password ) #로그인
    s.sendmail(sendEmail, recvEmail, msg.as_string()) #메일 전송, 문자열로 변환하여 보냅니다.
    s.close() #smtp 서버 연결을 종료합니다.