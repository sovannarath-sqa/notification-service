from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from credential.services.property_profile_service import PropertyProfileService

class PropertyProfileView(View):
    
    @csrf_exempt
    def create_property(request):
        """
        Create a new property profile.
        """
        try:
            name = request.POST.get('name')
            logo = request.FILES.get('logo')  # Assuming file upload for the logo
            description = request.POST.get('description')
            
            if not name:
                return JsonResponse({"error": "Name is required"}, status=400)
            
            property_profile = PropertyProfileService.create_property_profile(name, logo, description)
            
            if isinstance(property_profile, dict) and property_profile.get('error'):
                return JsonResponse(property_profile, status=400)

            return JsonResponse({"message": "Property profile created", "id": property_profile.id}, status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    def update_property(request, property_profile_id):
        """
        Update an existing property profile.
        """
        try:
            name = request.POST.get('name')
            logo = request.FILES.get('logo')  # Optional file upload
            description = request.POST.get('description')

            property_profile = PropertyProfileService.update_property_profile(property_profile_id, name, logo, description)
            
            if isinstance(property_profile, dict) and property_profile.get('error'):
                return JsonResponse(property_profile, status=400)

            return JsonResponse({"message": "Property profile updated", "id": property_profile.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    def delete_property(request, property_profile_id):
        """
        Soft delete a property profile.
        """
        try:
            property_profile = PropertyProfileService.delete_property_profile(property_profile_id)
            
            if isinstance(property_profile, dict) and property_profile.get('error'):
                return JsonResponse(property_profile, status=404)

            return JsonResponse({"message": "Property profile deleted"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    def get_property_detail(request, property_profile_id):
        """
        Retrieve a property profile by its ID.
        """
        try:
            property_profile = PropertyProfileService.get_property_profile(property_profile_id)
            
            if isinstance(property_profile, dict) and property_profile.get('error'):
                return JsonResponse(property_profile, status=404)

            # Serialize the property profile to return JSON (this assumes a simple dictionary or model serialization)
            return JsonResponse({
                "id": property_profile.id,
                "name": property_profile.name,
                "logo": property_profile.logo.url if property_profile.logo else None,
                "description": property_profile.description,
                "created_at": property_profile.created_at,
                "deleted_at": property_profile.deleted_at
            })
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    def get_all_properties(request):
        """
        Get all property profiles.
        """
        try:
            property_profiles = PropertyProfileService.get_all_property_profiles()
            
            # Serialize all property profiles to return JSON
            property_profile_data = [
                {
                    "id": profile.id,
                    "name": profile.name,
                    "logo": profile.logo,
                    "suitebook_id": profile.suitebook_id,
                    "aos_slug": profile.aos_slug,
                    "aos_organization_name": profile.aos_organization_name,
                    "aos_organization_slug": profile.aos_organization_slug,
                    "description": profile.description,
                    "created_at": profile.created_at,
                    "deleted_at": profile.deleted_at
                } for profile in property_profiles
            ]
            
            return JsonResponse(property_profile_data, safe=False)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)