import os

ROOT_CA = (
    "/Users/chiraag/Library/Application Support/Caddy/pki/authorities/local/root.crt"
)

os.environ["REQUESTS_CA_BUNDLE"] = ROOT_CA

from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

BASE_URL = "https://192.168.0.12"

client = LegacyApplicationClient(client_id="")
oauth = OAuth2Session(client=client)

resp = oauth.get(BASE_URL + "/users/me")
print(resp.content)

token = oauth.fetch_token(
    token_url=BASE_URL + "/token", username="johndoe", password="secret"
)


resp = oauth.get(BASE_URL + "/users/me")
print(resp.content)
