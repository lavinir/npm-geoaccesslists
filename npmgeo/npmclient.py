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
        response_json = response.json()
        token = response_json["token"]
        return token
    else:
        print(f"Error getting token. ({response.status_code})")    

def get_access_list_id(name: str, token: str) -> str:
    global BASE_URL, BASE_PORT
    url = f"http://{BASE_URL}:{BASE_PORT}/api/nginx/access-lists"
    headers = {
        'Authorization' : f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    if (response.status_code == 200):
        response_json = response.json()
        matching_rule_ids = [rule["id"] for rule in response_json if rule["name"].lower() == name.lower()]
        if matching_rule_ids:
            return matching_rule_ids[0]
        else:
            print(matching_rule_ids)
    else:
        print(f"Error getting access rules. ({response.status_code})")
        

def add_access_list(name: str, token: str, existing_rule_id: str, *clients: Access_Rule_Client) -> int:
    payload = { "name" : name,
                "satisfy_any" : False,
                "pass_auth" : False,
                "items": [],
                "clients": [{'address': rule.address, 'directive': rule.directive} for rule in clients]                 
            }
    
    headers = {
        'Authorization' : f'Bearer {token}'
    }

    if existing_rule_id is None:
        url = f"http://{BASE_URL}:{BASE_PORT}/api/nginx/access-lists"
        response = requests.post(url, json=payload, headers=headers)
    else:
        print(f"adding to ruleid : {existing_rule_id}")
        url = f"http://{BASE_URL}:{BASE_PORT}/api/nginx/access-lists/{existing_rule_id}"
        response = requests.put(url, json=payload, headers=headers)

    if response.status_code in [200, 201]:
        response_json = response.json()
        id = response_json["id"]
        print(f'Successfully {"updated" if existing_rule_id else "created"} rule (id: {id})')
        return id
    else:
        print(f"Error adding access list. ({response.status_code})")    
        return -1

