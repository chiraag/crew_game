import os
import secrets
from distutils.util import strtobool

from dotenv import load_dotenv

load_dotenv("data/.env")

LOCAL_DEV = strtobool(os.environ["LOCAL_DEV"])
BASE_URL = os.environ["BASE_URL"]

SECRET_KEY = os.environ["JWT_SECRET"] if LOCAL_DEV else secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REGISTER_TOKEN_EXPIRE_MINUTES = 30
RESET_TOKEN_EXPIRE_MINUTES = 15

API_VERSION = "v1"

ALLOW_REGISTRATION = True

TEST_EMAIL_ALLOWED = strtobool(os.environ["TEST_EMAIL_ALLOWED"])
TEST_EMAIL_ADDR = os.environ["TEST_EMAIL_ADDR"]
