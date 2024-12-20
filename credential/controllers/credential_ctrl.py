from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from credential.services.credential_service import CredentialService
import json

class CredentialView(View):

    @csrf_exempt  # Optionally use if you are using forms with no CSRF tokens (though it's not recommended for production)
    def create_credential(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            property_id = data.get('property')
            ota_id = data.get('ota')
            username = data.get('username')
            password = data.get('password')

            if not all([property_id, ota_id, username, password]):
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

            credential = CredentialService.create_credential(
                property=property_id,
                ota=ota_id,
                username=username,
                password=password
            )
            return JsonResponse({
                'id': credential.id,
                'username': credential.username,
                'property': credential.property.id,
                'ota': credential.ota.id,
                'is_active': credential.is_active
            }, status=201)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Failed to create credential: ' + str(e)}, status=500)
        
    def update_credential(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            credential_id = kwargs.get('credential_id')
            username = data.get('username')
            password = data.get('password')
            is_active = data.get('is_active')

            credential = CredentialService.update_credential(
                credential_id=credential_id,
                username=username,
                password=password,
                is_active=is_active
            )

            return JsonResponse({
                'id': credential.id,
                'username': credential.username,
                'is_active': credential.is_active
            }, status=200)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Failed to update credential: ' + str(e)}, status=500)
        
    def delete_credential(request, *args, **kwargs):
        try:
            credential_id = kwargs.get('credential_id')
            result = CredentialService.delete_credential(credential_id=credential_id)
            if result:
                return JsonResponse({'message': 'Credential deleted successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Failed to delete credential'}, status=400)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Failed to delete credential: ' + str(e)}, status=500)
        
    def get_credential_detail(request, *args, **kwargs):
        try:
            active_credentials = CredentialService.get_active_credentials()
            credentials_data = [
                {
                    'id': credential.id,
                    'username': credential.username,
                    'property_id': credential.property_id.id,
                    'ota_id': credential.ota_id.id,
                    'is_active': credential.is_active
                }
                for credential in active_credentials
            ]
            return JsonResponse({'credentials': credentials_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': 'Failed to fetch active credentials: ' + str(e)}, status=500)
        
    def get_all_credentials (request) :
        try:
            print("List all!")
            credentials = CredentialService.get_all_credentials()

            # Create a list of profiles to return in the response
            credentials_data = [
                {
                    'id': credential.id,
                    'username': credential.username,
                    'password': credential.password,
                    'property': {'id': credential.property.id, 'name': credential.property.name},
                    'ota': {'id': credential.ota.id, 'name':credential.ota.name},
                }
                for credential in credentials
            ]

            return JsonResponse(credentials_data, safe=False)
        except Exception as e :
            return JsonResponse({'error' : 'Failed to retrieve credentials data.' + str(e)}, status=500)
