from django.http import JsonResponse, HttpResponse
from credential.dto.credential_dto import CredentialDTO
from automate_login.services.auto_login_service import AutoLoginService
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json

class AutomateLoginView (View) :   
    
    @csrf_exempt
    def agoda_login_view(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            channel_id = data.get('channel_id')
            reservations = data.get('reservation_id')
            channel_name = data.get('channel')
            browser = data.get('browser')

            if not all([username, password, channel_name, channel_id, reservations]):
                return JsonResponse({"error": "Missing required parameters"}, status=400)

            credential = CredentialDTO(
                username = username, 
                password = password, 
                channel_name = channel_name, 
                channel_id = channel_id, 
                reservations = reservations
            )

            try:
                AutoLoginService.agoda_login(browser=browser, credential=credential, reservations=reservations)
                return JsonResponse({"message": "Login and message sending successful"})
            
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        return HttpResponse(status=405)

    @csrf_exempt
    def airbnb_login_view(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            channel_id = data.get('channel_id')
            reservations = data.get('reservation_id')
            channel_name = data.get('channel')
            browser = data.get('browser')

            if not all([username, password, channel_name, channel_id, reservations]):
                return JsonResponse({"error": "Missing required parameters"}, status=400)

            credential = CredentialDTO(
                username = username, 
                password = password, 
                channel_name = channel_name, 
                channel_id = channel_id, 
                reservations = reservations
            )
        
            try:
                AutoLoginService.airbnb_login(browser=browser, credential=credential)
                return JsonResponse({"message": "Login and message sending successful"})
            
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        return HttpResponse(status=405)

    @csrf_exempt
    def rakuten_login_view(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            channel_id = data.get('channel_id')
            reservations = data.get('reservation_id')
            channel_name = data.get('channel')
            browser = data.get('browser')

            if not all([username, password, channel_name, channel_id, reservations]):
                return JsonResponse({"error": "Missing required parameters"}, status=400)

            credential = CredentialDTO(
                username = username, 
                password = password, 
                channel_name = channel_name, 
                channel_id = channel_id, 
                reservations = reservations
            )

            try:
                AutoLoginService.rakuten_login(browser=browser, credential=credential)
                return JsonResponse({"message": "Login and message sending successful"})
            
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        return HttpResponse(status=405)
    