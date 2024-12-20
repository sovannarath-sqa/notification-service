from django.shortcuts import render
from one_password.services.one_password_service import OnePasswordSecret
from django.http import JsonResponse

def secure_view(request):
    secret_data = OnePasswordSecret.get_1password_secret('your-item-id')
    api_key = secret_data.get('fields', {}).get('API_KEY', {}).get('value')

    return JsonResponse({"api_key": api_key})
