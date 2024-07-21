import os
from .common import *

DEBUG = False

# SECRET_KEY
SECRET_KEY = os.getenv("SECRET_KEY")

# mysql_DB
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


# #
# AWS_ACCESS_KEY_ID = "Access key ID 입력"  # .csv 파일에 있는 내용을 입력 Access key ID
# AWS_SECRET_ACCESS_KEY = (
#     "Secret acess Key 입력"  # .csv 파일에 있는 내용을 입력 Secret access key
# )
# AWS_REGION = "ap-northeast-2"
#
# # S3 Storages
# AWS_STORAGE_BUCKET_NAME = "lee-teset-bucket"  # 설정한 버킷 이름
# AWS_S3_CUSTOM_DOMAIN = "%s.s3.%s.amazonaws.com" % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
# AWS_S3_OBJECT_PARAMETERS = {
#     "CacheControl": "max-age=86400",
# }
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# MEDIA_ROOT = os.path.join(BASE_DIR, "path/to/store/my/files/")
