from os import environ as env
from sys import stdin
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
#import re

static_data = """

Account Name: refurbtest
Account Email: refurbtest@company.com
Plan: Basic
Device Names: IMEI

"""

def use_default_env_creds():
    """ uses os.environ as env to get credentials from external .env file"""
    access_token_url = env.get("ACCESS_TOKEN_URL")
    client_id = env.get("CLIENT_ID")
    client_secret = env.get("CLIENT_SECRET")
    return {"access_token_url": access_token_url,
            "client_id": client_id,
            "client_secret": client_secret
            }

def authenticate(*, creds) -> dict:
    """Takes credentials as a dict. Returns a dict with the authenticated OAuth2Session
    which is valid for 30 min. You must time externally and reauthenticate
    when necessary. Also returns your headers as a dict.
    """
    headers = {"Content-Type": "application/json"}
    
    # probably good idea to do data validation on creds one day
    # BUT THAT IS NOT THIS DAY
    
    # oauth instead of requests
    client = BackendApplicationClient(client_id=creds["client_id"])
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=creds["access_token_url"], 
                              client_id=creds["client_id"],
                              client_secret=creds["client_secret"]
                              )
    headers["Authorization"] = f"Bearer {token}"
    
    return {"session": oauth, "headers": headers}

def query_api(*, url, session,
              headers, body):
    resp = session.post(url=url,
                         headers=headers,
                         json=body
                         )
    return resp

def validate_response(*, response):
    print(response.text)
    try:
        code = response.json()["statusCode"]
        if code == 406:
            return (0,)
        else:
            return (2, f"{code} - {response.text}")
    except:
        # returns customer info
        return (1,)
    
def parser(*, data):
    """Takes input from command-line as a list of lines, 
    parses line-by-line for pairings of
    IMEIs (15 digits) and ICCIDs (19 digits) and returns them as a tuple
    of form (imei, iccid). DOES NOT USE REGEX
    
    Raises TypeError if more than 2 things are in each line
    """
    #imei_pattern = r"[0-9]{15}"
    #iccid_pattern = r"[0-9]{19}"
    output = []
    for line in data:
        values = line.split()
        if len(values) > 2:
            raise TypeError
        if len(values[0]) == 15:
            output.append(tuple(values))
        else:
            output.append(tuple(values[::-1]))
    return output

def output(*, items: dict, filename=''):
    
    data = ""
    data += static_data
    
    successful_iccids = []
    data += "\n\nTo Add:\n\n"
    if items["successful"]:
        for imei, iccid in items["successful"]:
            data += f"{imei}\n"
            successful_iccids.append(iccid)
        else:
            data += "\n\nICCIDs to check:\n\n"
            for iccid in successful_iccids:
                data += f"{iccid}\n"
    else:
        data += "None\n"
            
    data += "\n\nDevices to remove from refurb queue\n\n"
    if items["taken"]:
        for imei, iccid in items["taken"]:
            data += f"{imei} - {iccid}\n"
    else:
        data += "None\n"
    
    data += "\n\nErrors to look into\n\n"
    if items["failed"]:
        for imei, iccid, context in items["failed"]:
            data += f"{imei} - {iccid} : {context}\n"
    else:
        data += "None\n"
    
    if filename:
        with open(filename, "w") as f:
            f.write(data)
    print(data)
    
if __name__ == "__main__":
    successful = []
    taken = []
    failed = []
    url = "https://api.companylistener.com/v2/device/info"
    
    print("Enter input, press CTRL+D to finish > ")
    input_data = stdin.readlines()
    
    parsed_data = parser(data=input_data)
    
    creds = use_default_env_creds()
    
    d = authenticate(creds=creds)
    session = d["session"]
    headers = d["headers"]
    
    for imei, iccid in parsed_data:
        body = {"imei": imei}
        resp = query_api(url=url, session=session, headers=headers, body=body)
        print(imei)
        
        validation = validate_response(response=resp)
        if validation[0] == 0:
            successful.append((imei, iccid))
        elif validation[0] == 1:
            taken.append((imei, iccid))
        else:
            failed.append((imei, iccid, validation[1]))
        
    output(items={"successful": successful, "taken": taken, "failed": failed})