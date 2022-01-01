import os

from dotenv import load_dotenv
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

load_dotenv()
BASE_URL = os.environ["BASE_URL"]

client = LegacyApplicationClient(client_id="")
oauth = OAuth2Session(client=client)

resp = oauth.get(BASE_URL + "/users/me")
print(resp.content)

token = oauth.fetch_token(
    token_url=BASE_URL + "/token", username="johndoe", password="secret"
)


resp = oauth.get(BASE_URL + "/users/me")
print(resp.content)
