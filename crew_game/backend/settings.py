import os
from distutils.util import strtobool

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["BACKEND_JWT_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REGISTER_TOKEN_EXPIRE_MINUTES = 30
RESET_TOKEN_EXPIRE_MINUTES = 15

API_VERSION = "v1"

ALLOW_REGISTRATION = True

TEST_EMAIL_ALLOWED = strtobool(os.environ["TEST_EMAIL_ALLOWED"])
TEST_EMAIL_ADDR = os.environ["TEST_EMAIL_ADDR"]
