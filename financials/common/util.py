import string
import secrets
import requests

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(secrets.choice(letters) for i in range(length))
    return result_str

def get_monzo_request( endpoint: string, auth_code: string ):
    return requests.get(
        url="https://api.monzo.com" + endpoint,
        headers={
            "Authorization": "Bearer " + auth_code
        }
    )