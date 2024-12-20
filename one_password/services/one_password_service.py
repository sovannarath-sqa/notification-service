from django.conf import settings
import requests

class OnePasswordSecret :
    def get_1password_secret(item_id):
        url = f"{settings.OP_CONNECT_URL}/v1/items/{item_id}"
        headers = {
            'Authorization': f'Bearer {settings.OP_API_KEY}',
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to retrieve secret: {response.status_code}")
            return None
