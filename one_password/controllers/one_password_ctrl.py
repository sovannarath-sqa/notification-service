import json
from django.http import JsonResponse
from django.views import View
from one_password.services.one_password_service import OnePasswordSecret


class GetSecretView(View):

    def get_1password_secret (request, secret_name):
        try:
            secret_value = OnePasswordSecret.get_one_password_secret(secret_name)
            return JsonResponse({'secret': secret_value}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
