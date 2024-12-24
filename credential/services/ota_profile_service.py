#from django.db import transaction
from credential.models.otaprofile import OTAProfile
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class OTAProfileService:
    @staticmethod
    def create_ota_profile(name, logo, description=None):
        """
        Creates a new OTAProfile record.
        """
        try:
            ota_profile = OTAProfile.objects.create(
                name=name,
                logo=logo,
                description=description
            )
            return ota_profile
        except Exception as e:
            raise Exception(f"Error creating OTAProfile: {str(e)}")

    @staticmethod
    def get_ota_profile_by_id(profile_id):
        """
        Fetches an OTAProfile by its ID.
        """
        try:
            return OTAProfile.objects.get(id=profile_id)
        except OTAProfile.DoesNotExist:
            raise ObjectDoesNotExist(f"OTAProfile with ID {profile_id} not found.")

    @staticmethod
    def get_all_ota_profiles():
        """
        Returns all OTAProfile records, ordered by created_at (newest first).
        """
        return OTAProfile.objects.all()

    @staticmethod
    def update_ota_profile(profile_id, name=None, logo=None, description=None):
        """
        Updates an OTAProfile by ID.
        """
        try:
            ota_profile = OTAProfile.objects.get(id=profile_id)
            if name:
                ota_profile.name = name
            if logo:
                ota_profile.logo = logo
            if description is not None:
                ota_profile.description = description
            ota_profile.save()
            return ota_profile
        except OTAProfile.DoesNotExist:
            raise ObjectDoesNotExist(f"OTAProfile with ID {profile_id} not found.")
        except Exception as e:
            raise Exception(f"Error updating OTAProfile: {str(e)}")

    @staticmethod
    def delete_ota_profile(profile_id):
        """
        Marks an OTAProfile as deleted (soft delete).
        """
        try:
            ota_profile = OTAProfile.objects.get(id=profile_id)
            ota_profile.deleted_at = timezone.now()  # Mark the deletion timestamp
            ota_profile.save()
            return ota_profile
        except OTAProfile.DoesNotExist:
            raise ObjectDoesNotExist(f"OTAProfile with ID {profile_id} not found.")
        except Exception as e:
            raise Exception(f"Error deleting OTAProfile: {str(e)}")

    @staticmethod
    def restore_ota_profile(profile_id):
        """
        Restores a soft-deleted OTAProfile (sets deleted_at to None).
        """
        try:
            ota_profile = OTAProfile.objects.get(id=profile_id)
            ota_profile.deleted_at = None
            ota_profile.save()
            return ota_profile
        except OTAProfile.DoesNotExist:
            raise ObjectDoesNotExist(f"OTAProfile with ID {profile_id} not found.")
        except Exception as e:
            raise Exception(f"Error restoring OTAProfile: {str(e)}")