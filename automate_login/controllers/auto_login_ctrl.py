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
            # Extract the credentials and browser from the request
            username = data.get('username')
            password = data.get('password')
            channel_id = data.get('channel_id')
            reservation_id = data.get('reservation_id')
            browser = 'Firefox'  

            if not all([username, password, channel_id, reservation_id]):
                return JsonResponse({"error": "Missing required parameters"}, status=400)

            # Create a CredentialDTO object
            credential = CredentialDTO(username=username, password=password, channel_id=channel_id, reservation_id=reservation_id)
        
            try:
                # Call the agoda_login method from AutoLoginService
                AutoLoginService.agoda_login(browser=browser, credential=credential)
                return JsonResponse({"message": "Login and message sending successful"})
        
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        return HttpResponse(status=405)  # Method not allowed if not a POST request

    @csrf_exempt
    def airbnb_login_view(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            # Extract the credentials and browser from the request
            username = data.get('username')
            password = data.get('password')
            channel_id = data.get('channel_id')
            reservation_id = data.get('reservation_id')
            browser = 'Firefox'
        
            if not all([username, password, channel_id, reservation_id]):
                return JsonResponse({"error": "Missing required parameters"}, status=400)

            # Create a CredentialDTO object
            credential = CredentialDTO(username=username, password=password, channel_id=channel_id, reservation_id=reservation_id)
        
            try:
                # Call the airbnb_login method from AutoLoginService
                AutoLoginService.airbnb_login(browser=browser, credential=credential)
                return JsonResponse({"message": "Login successful"})
        
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        return HttpResponse(status=405)  # Method not allowed if not a POST request

    @csrf_exempt
    def rakuten_login_view(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            # Extract the credentials and browser from the request
            username = data.get('username')
            password = data.get('password')
            channel_id = data.get('channel_id')
            reservation_id = data.get('reservation_id')
            browser = 'Firefox'
        
            if not all([username, password, channel_id, reservation_id]):
                return JsonResponse({"error": "Missing required parameters"}, status=400)

            # Create a CredentialDTO object
            credential = CredentialDTO(username=username, password=password, channel_id=channel_id, reservation_id=reservation_id)
        
            try:
                # Call the rakuten_login method from AutoLoginService
                AutoLoginService.rakuten_login(browser=browser, credential=credential)
                return JsonResponse({"message": "Login successful"})
        
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        return HttpResponse(status=405)  # Method not allowed if not a POST request
    
