import json
from django.http import JsonResponse
from django.views import View
from one_password.services.one_password_service import OnePasswordImplement


class GetSecretView(View):

    def get_item_list (request) :
        try:
            secret_value = OnePasswordImplement.get_list()
            return JsonResponse({'secret': secret_value}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def get_item_secret (request):
        try:
            secret_value = OnePasswordImplement.get_secret()
            return JsonResponse({'secret': secret_value}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
