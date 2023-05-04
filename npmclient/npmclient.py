import requests
import json
from collections import namedtuple

BASE_URL = None
BASE_PORT = 81

Access_Rule_Client = namedtuple('Access_Rule_Client', ['address', 'directive'])

def get_auth_token(emailAddress: str, password: str) -> str:
    global BASE_URL, BASE_PORT
    url = f"http://{BASE_URL}:{BASE_PORT}/api/tokens"
    payload = {"identity": emailAddress ,"secret":password}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        response_json = json.loads(response.text)
        token = response_json["token"]
        return token
    else:
        print(f"Error getting token. ({response.status_code})")    

def add_access_list(name: str, token: str, *clients: Access_Rule_Client) -> int:
    payload = { "name" : name,
                "satisfy_any" : False,
                "pass_auth" : False,
                "items": [],
                "clients": [{'address': rule.address, 'directive': rule.directive} for rule in clients]                 
            }
    
    url = f"http://{BASE_URL}:{BASE_PORT}/api/nginx/access-lists"
    headers = {
        'Authorization' : f'Bearer {token}'
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code in [200, 201]:
        response_json = response.json()
        id = response_json["id"]
        print(f'Successfully created new rule (id: {id})')
        return id
    else:
        print(f"Error adding access list. ({response.status_code})")    
        return -1
