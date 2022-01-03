import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["BACKEND_JWT_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

API_VERSION = "v1"

ALLOW_REGISTRATION = True

fake_users_db = {
    "johndoe": {
        "id": 0,
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_active": True,
    }
}
