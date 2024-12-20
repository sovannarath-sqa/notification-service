from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from credential.services.ota_profile_service import OTAProfileService
import json

class OTAProfileView(View):
    @csrf_exempt
    def create_ota_profile(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                name = data.get('name')
                logo = data.get('logo')
                description = data.get('description', None)
            
                # Create the OTA profile using the service
                ota_profile = OTAProfileService.create_ota_profile(name, logo, description)
            
                # Respond with the created profile data
                return JsonResponse({
                    'id': ota_profile.id,
                    'name': ota_profile.name,
                    'logo': ota_profile.logo,
                    'description': ota_profile.description
                }, status=201)

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Invalid HTTP method. POST required.'}, status=405)
        
    
    def get_ota_profile(request, profile_id):
        try:
            # Fetch the OTA profile by ID using the service
            ota_profile = OTAProfileService.get_ota_profile_by_id(profile_id)
        
            return JsonResponse({
                'id': ota_profile.id,
                'name': ota_profile.name,
                'logo': ota_profile.logo,
                'description': ota_profile.description
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=404)
    

    def get_all_ota_profiles(request):
        try:
            # Fetch all OTA profiles using the service
            ota_profiles = OTAProfileService.get_all_ota_profiles()
        
            # Create a list of profiles to return in the response
            profiles_data = [{
                'id': profile.id,
                'name': profile.name,
                'logo': profile.logo,
                'description': profile.description
            } for profile in ota_profiles]

            return JsonResponse(profiles_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    @csrf_exempt
    def update_ota_profile(request, profile_id):
        if request.method == 'PATCH':
            try:
                data = json.loads(request.body)
                name = data.get('name')
                logo = data.get('logo')
                description = data.get('description', None)
            
                # Update the OTA profile using the service
                ota_profile = OTAProfileService.update_ota_profile(profile_id, name, logo, description)
            
                # Respond with the updated profile data
                return JsonResponse({
                    'id': ota_profile.id,
                    'name': ota_profile.name,
                    'logo': ota_profile.logo,
                    'description': ota_profile.description
                })

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Invalid HTTP method. PATCH required.'}, status=405)
    
    def delete_ota_profile(request, profile_id):
        if request.method == 'DELETE':
            try:
                # Soft delete the OTA profile using the service
                ota_profile = OTAProfileService.delete_ota_profile(profile_id)
            
                return JsonResponse({
                    'id': ota_profile.id,
                    'name': ota_profile.name,
                    'status': 'deleted'
                })
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=404)
        else:
            return JsonResponse({'error': 'Invalid HTTP method. DELETE required.'}, status=405)

    def restore_ota_profile(request, profile_id):
        if request.method == 'POST':
            try:
                # Restore the soft-deleted OTA profile using the service
                ota_profile = OTAProfileService.restore_ota_profile(profile_id)
            
                return JsonResponse({
                    'id': ota_profile.id,
                    'name': ota_profile.name,
                    'status': 'restored'
                })
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=404)
        else:
            return JsonResponse({'error': 'Invalid HTTP method. POST required.'}, status=405)
    

