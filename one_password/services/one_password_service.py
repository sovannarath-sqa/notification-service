from onepassword import *
from django.conf import settings
import requests


class OnePasswordSecret :

    def get_one_password_secret (secret_name):
        token = settings.OP_SERVICE_ACCOUNT_TOKEN
        url = settings.OP_CONNECT_URL + secret_name

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            secret = response.json()
            return secret.get('value')
        else:
            raise Exception(f"Failed to retrieve secret")

    
    

