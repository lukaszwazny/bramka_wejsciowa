import os
import requests
import json

def safe_list_get (l, idx, default):
    try:
        return l[idx]
    except Exception:
        return default

def get_url():
    return os.environ['api_url']

def get_key():
    return os.environ['api_key']

def send_not_opening_command():
    url = os.environ['iotCentralHost'] + "ident/commands/open?api-version=1.0"
    payload = {'request': {isTrue: False}}
    payload=json.dumps(payload)
    headers = {
        'Authorization': os.environ['iotCentralToken'],
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response

def send_opening_command():
    url = os.environ['iotCentralHost'] + "ident/commands/open?api-version=1.0"
    payload = {'request': {isTrue: True}}
    payload=json.dumps(payload)
    headers = {
        'Authorization': os.environ['iotCentralToken'],
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response

def send_user_to_app(user):
    url = os.environ['iotCentralHost'] + "ap_ident/commands/gotUser?api-version=1.0"
    user.pop('additional_info')
    payload = {'request': user}
    payload=json.dumps(payload, default=str, ensure_ascii=False)
    headers = {
        'Authorization': os.environ['iotCentralToken'],
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response

def send_entrance_to_app(entrance):
    url = os.environ['iotCentralHost'] + "ap_ident/commands/gotEntrance?api-version=1.0"
    payload = {'request': entrance}
    payload=json.dumps(payload, default=str, ensure_ascii=False)
    headers = {
        'Authorization': os.environ['iotCentralToken'],
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response