import os
import json
import requests

def Function9(ident_nr):
    url = os.environ.get('API_HOST') + 'Function9'
    payload = json.dumps({'identificator_nr': str(ident_nr)})
    headers = {
        'Ocp-Apim-Subscription-Key': os.environ.get('OCP_APIM_SUBSCRIPTION_KEY'),
        'Content-Type': 'application/json'
    }
    return requests.request('POST', url, headers=headers, data=payload)

def Function8(ident_nr):
    url = os.environ.get('API_HOST') + 'Function8?identificator_nr=' + str(ident_nr)
    payload = {}
    headers = {
        'Ocp-Apim-Subscription-Key': os.environ.get('OCP_APIM_SUBSCRIPTION_KEY')
    }
    return requests.request('GET', url, headers=headers, data=payload)