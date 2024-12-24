from onepassword import *
from django.conf import settings
import subprocess
import requests
import json

class OnePasswordClient:
    def __init__(self, host, token):
        self.host = host
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def list_item(self, vault_id):
        url = f"{self.host}/v1/vaults/{vault_id}/items"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_item(self, vault_id, item_id):
        url = f"{self.host}/v1/vaults/{vault_id}/items/{item_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_item_field(self, vault_id, item_id, field_label):
        item = self.get_item(vault_id, item_id)
        for field in item.get("fields", []):
            if field.get("label") == field_label:
                return field.get("value")
        raise ValueError(f"Field '{field_label}' not found in item.")


class OnePasswordImplement :

    def __init__ (self) :
        self.op_client = OnePasswordClient(settings.OP_CONNECT_HOST, settings.OP_API_TOKEN)
        self.vault_id = "kdhewcrzpzqmwytjjhabiv4s4i"
        self.item_id = "5pxqegb7lxvtwltemz3iell5rq"
        self.field_label = "password"
    
    def get_list () : 
        object = OnePasswordImplement()
        return object.get_list(object.vault_id)

    def get_secret () :
        object = OnePasswordImplement()
        return object.op_client.get_item_field(
            object.vault_id, 
            object.item_id, 
            object.field_label
        )