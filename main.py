import data
import requests
import ssl
from requests.adapters import HTTPAdapter

user_agent, AUTH_URL = data.RIOTCLIENT, "https://auth.riotgames.com/api/v1/authorization"
user = ""
passw = ""

class SSLAdapter(HTTPAdapter):
    """
    Custom SSL adapter to manage SSL connections with specific configurations.
    """
    def init_poolmanager(self, *a, **k):
        """
        Initialize the pool manager with custom SSL context and cipher configurations.
        """
        c = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        c.set_ciphers(':'.join(data.CIPHERS))
        k['ssl_context'] = c
        return super().init_poolmanager(*a, **k)

def get_access_token():
    """
    Function to obtain the access token from Riot Games API.
    """
    s = requests.Session()
    s.mount('https://', SSLAdapter())
    s.headers = {"Accept-Language": "en-US,en;q=0.9", "Accept": "application/json, text/plain, */*",
                 'User-Agent': f'RiotClient/{user_agent} %s (Windows;10;;Professional, x64)'}
    d = {"acr_values": "urn:riot:bronze", "claims": "", "client_id": "riot-client", "nonce": "oYnVwCSrlS5IHKh7iI16oQ",
         "redirect_uri": "http://localhost/redirect", "response_type": "token id_token",
         "scope": "openid link ban lol_region"}
    h = {'Content-Type': 'application/json',
         'User-Agent': f'RiotClient/{user_agent} %s (Windows;10;;Professional, x64)'}
    r = s.post(AUTH_URL, json=d, headers=h, timeout=14)
    if r.status_code == 200:
        print("Authentication...")
        r2 = s.put(AUTH_URL, json={"type": "auth", "username": user, "password": passw}, headers=h, timeout=16)
        if r2.status_code == 200:
            response_data = r2.json()
            if "error" in response_data and response_data["error"] == "auth_failure":
                print(f"Authentication Failed: {user}:{passw}")
            else:
                print(f"Authentication Successful: {user}:{passw}")
                print(response_data)
        else:
            print(f"Request Failed: {r2.text}")
    else:
        print(f"Request Failed: {r.text}")

get_access_token()
