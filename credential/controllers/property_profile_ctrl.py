from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from credential.services.property_profile_service import PropertyProfileService
import json


class PropertyProfileView(View):

    @csrf_exempt
    def create_property(request):
        """
        Create a new property profile.
        """
        try:
            name = request.POST.get("name")
            logo = request.FILES.get("logo")
            suitebook_id = request.POST.get("suitebook_id")
            aos_slug = request.POST.get("aos_slug")
            aos_organization_name = request.POST.get("aos_organization_name")
            aos_organization_slug = request.POST.get("aos_organization_slug")
            description = request.POST.get("description")

            if not name:
                return JsonResponse({"error": "Name is required"}, status=400)

            property_profile = PropertyProfileService.create_property_profile(
                name=name,
                logo=logo,
                suitebook_id=suitebook_id,
                aos_slug=aos_slug,
                aos_organization_name=aos_organization_name,
                aos_organization_slug=aos_organization_slug,
                description=description,
            )

            if isinstance(property_profile, dict) and property_profile.get("error"):
                return JsonResponse(
                    {
                        "code": 400,
                        "status": "error",
                        "message": property_profile.get("error"),
                        "errors": [
                            {
                                "field": "unknown",
                                "message": property_profile.get("error"),
                            }
                        ],
                        "data": [],
                    },
                    status=400,
                )

            return JsonResponse(
                {
                    "code": 201,
                    "status": "success",
                    "message": "Property profile created successfully",
                    "data": {
                        "id": property_profile.id,
                        "name": property_profile.name,
                        "logo": property_profile.logo,
                        "suitebook_id": property_profile.suitebook_id,
                        "aos_slug": property_profile.aos_slug,
                        "aos_organization_name": property_profile.aos_organization_name,
                        "aos_organization_slug": property_profile.aos_organization_slug,
                        "description": property_profile.description,
                        "permissions": [],
                        "status": "active",
                        "created_at": property_profile.created_at.isoformat(),
                        "created_by": "system",
                        "updated_at": property_profile.updated_at.isoformat(),
                        "updated_by": "system",
                        "deleted_at": None,
                        "deleted_by": None,
                    },
                },
                status=201,
            )

        except Exception as e:
            return JsonResponse(
                {
                    "code": 500,
                    "status": "error",
                    "message": str(e),
                    "errors": [{"field": "unknown", "message": str(e)}],
                    "data": [],
                },
                status=500,
            )

    @csrf_exempt
    def update_property(request, property_profile_id):

        try:
            # Parse JSON body
            body = json.loads(request.body)
            print("Parsed Request Body: ", body)

            # Extract values from the parsed JSON body
            name = body.get("name")
            suitebook_id = body.get("suitebook_id")
            aos_slug = body.get("aos_slug")
            aos_organization_name = body.get("aos_organization_name")
            aos_organization_slug = body.get("aos_organization_slug")
            description = body.get("description")
            logo = request.FILES.get("logo")

            if not name:
                return JsonResponse({"error": "Name is required"}, status=400)

            # Update the property profile
            property_profile = PropertyProfileService.update_property_profile(
                property_profile_id,
                name=name,
                logo=logo,
                suitebook_id=suitebook_id,
                aos_slug=aos_slug,
                aos_organization_name=aos_organization_name,
                aos_organization_slug=aos_organization_slug,
                description=description,
            )

            if isinstance(property_profile, dict) and property_profile.get("error"):
                return JsonResponse(
                    {
                        "code": 400,
                        "status": "error",
                        "message": property_profile.get("error"),
                        "errors": [
                            {
                                "field": "unknown",
                                "message": property_profile.get("error"),
                            }
                        ],
                        "data": [],
                    },
                    status=400,
                )

            return JsonResponse(
                {
                    "code": 200,
                    "status": "success",
                    "message": "Property profile updated successfully",
                    "data": {
                        "id": property_profile.id,
                        "name": property_profile.name,
                        "logo": property_profile.logo,
                        "suitebook_id": property_profile.suitebook_id,
                        "aos_slug": property_profile.aos_slug,
                        "aos_organization_name": property_profile.aos_organization_name,
                        "aos_organization_slug": property_profile.aos_organization_slug,
                        "description": property_profile.description,
                        "permissions": [],
                        "status": "active",
                        "created_at": property_profile.created_at.isoformat(),
                        "created_by": "system",
                        "updated_at": property_profile.updated_at.isoformat(),
                        "updated_by": "system",
                        "deleted_at": None,
                        "deleted_by": None,
                    },
                },
                status=200,
            )

        except Exception as e:
            return JsonResponse(
                {
                    "code": 500,
                    "status": "error",
                    "message": str(e),
                    "errors": [{"field": "unknown", "message": str(e)}],
                    "data": [],
                },
                status=500,
            )

    def delete_property(request, property_profile_id):
        """
        Soft delete a property profile.
        """
        try:
            property_profile = PropertyProfileService.delete_property_profile(
                property_profile_id
            )

            if isinstance(property_profile, dict) and property_profile.get("error"):
                return JsonResponse(property_profile, status=404)

            return JsonResponse({"message": "Property profile deleted"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def get_property_detail(request, property_profile_id):
        """
        Retrieve a property profile by its ID.
        """
        try:
            property_profile = PropertyProfileService.get_property_profile(
                property_profile_id
            )

            if isinstance(property_profile, dict) and property_profile.get("error"):
                return JsonResponse(property_profile, status=404)

            return JsonResponse(
                {
                    "id": property_profile.id,
                    "name": property_profile.name,
                    "logo": (
                        property_profile.logo.url if property_profile.logo else None
                    ),
                    "description": property_profile.description,
                    "created_at": property_profile.created_at,
                    "deleted_at": property_profile.deleted_at,
                }
            )

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
                    "deleted_at": profile.deleted_at,
                }
                for profile in property_profiles
            ]

            return JsonResponse(
                {
                    "code": 200,
                    "status": "success",
                    "message": "Property profiles retrieved successfully",
                    "data": property_profile_data,
                }
            )
        except PropertyProfileService.DoesNotExist:
            return JsonResponse(
                {
                    "code": 404,
                    "status": "error",
                    "message": "No property profiles found",
                    "errors": [
                        {
                            "field": "unknown",
                            "message": "No property profiles available",
                        }
                    ],
                    "data": [],
                },
                status=404,
            )

        except Exception as e:
            return JsonResponse(
                {
                    "code": 500,
                    "status": "error",
                    "message": str(e),
                    "errors": [{"field": "unknown", "message": str(e)}],
                    "data": [],
                },
                status=500,
            )
