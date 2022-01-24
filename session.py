from os import environ as env
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

class CompanySession:
    
    def __init__(self):
        self.session = None
        self.creds = None
        self.token = None
        
        
        
        if not self.session:
            self.reauthenticate()
    
    def create_session(self):
        self.get_credentials()
        client = BackendApplicationClient(client_id=self.creds["client_id"])
        session = OAuth2Session(client=client)
        self.session = session
    
    def get_credentials(self):
        access_token_url = env.get("ACCESS_TOKEN_URL")
        client_id = env.get("CLIENT_ID")
        client_secret = env.get("CLIENT_SECRET")
        
        creds = {"access_token_url": access_token_url,
                 "client_id": client_id,
                 "client_secret": client_secret
        }
        self.creds = creds

    def get_token(self):
        token = self.session.fetch_token(token_url=self.creds["access_token_url"],
                                         client_id=self.creds["client_id"],
                                         client_secret=self.creds["client_secret"]
                                         )
        self.token = token
        CompanySession.headers["Authorization"] = f"Bearer {token}"
    
    def reauthenticate(self):
        self.create_session()
        self.get_token()