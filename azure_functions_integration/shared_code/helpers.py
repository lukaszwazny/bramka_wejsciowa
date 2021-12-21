import os

def safe_list_get (l, idx, default):
    try:
        return l[idx]
    except Exception:
        return default

def get_url():
    return os.environ['api_url']

def get_key():
    return os.environ['api_key']