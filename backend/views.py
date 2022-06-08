import requests
from django.conf import settings

def verify_token(token):
    """
    Simple method for verifying your
    token data. This method only verifies
    your `access` token. A 200 HTTP status
    means success, anything else means failure.
    """

    data = {
        "token": token
    }
    endpoint = "http://localhost:5000/Auth/token/verify/" 
    r = requests.post(endpoint, json=data)

    if r.status_code == 200: # 토큰이 유효하면
        return True
    else: # access token이 무효할 시, refresh token을 통해서 access token 재발행 필요
        return False

def refrech_token(token):
    data = {
        "token": token
    }
    endpoint = "http://localhost:5000/Auth/token/refresh/" 
    r = requests.post(endpoint, json=data)
    print(r)
    print(r.json)
    if r.status_code == 200: # 토큰이 유효하면
        return True
    else: # access token이 무효할 시, refresh token을 통해서 access token 재발행 필요
        return False