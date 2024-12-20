from django.db import IntegrityError
from credential.models.propertyprofile import PropertyProfile
from django.utils.timezone import now

class PropertyProfileService:
    
    @staticmethod
    def create_property_profile(name, logo=None, description=None):
        """
        Create a new PropertyProfile instance.
        """
        try:
            property_profile = PropertyProfile.objects.create(
                name=name,
                logo=logo,
                description=description
            )
            return property_profile
        except IntegrityError as e:
            # Handle any database-related errors
            return {"error": str(e)}

    @staticmethod
    def update_property_profile(property_profile_id, name=None, logo=None, description=None):
        """
        Update an existing PropertyProfile instance by ID.
        """
        try:
            property_profile = PropertyProfile.objects.get(id=property_profile_id)
            if name:
                property_profile.name = name
            if logo:
                property_profile.logo = logo
            if description:
                property_profile.description = description
            property_profile.save()
            return property_profile
        except PropertyProfile.DoesNotExist:
            return {"error": "PropertyProfile not found"}
        except IntegrityError as e:
            return {"error": str(e)}

    @staticmethod
    def delete_property_profile(property_profile_id):
        """
        Soft delete a PropertyProfile instance (set the deleted_at timestamp).
        """
        try:
            property_profile = PropertyProfile.objects.get(id=property_profile_id)
            property_profile.deleted_at = now()  # Soft delete the object by setting the deleted_at field
            property_profile.save()
            return property_profile
        except PropertyProfile.DoesNotExist:
            return {"error": "PropertyProfile not found"}

    @staticmethod
    def get_property_profile(property_profile_id):
        """
        Retrieve a PropertyProfile instance by ID.
        """
        try:
            property_profile = PropertyProfile.objects.get(id=property_profile_id)
            return property_profile
        except PropertyProfile.DoesNotExist:
            return {"error": "PropertyProfile not found"}

    @staticmethod
    def get_all_property_profiles():
        """
        Get all property profiles, excluding those that have been soft deleted.
        """
        return PropertyProfile.objects.filter(deleted_at__isnull=True).order_by('-created_at')
