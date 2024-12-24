from django.db import IntegrityError
from credential.models.credential import Credential
from credential.models.otaprofile import OTAProfile
from credential.models.propertyprofile import PropertyProfile
from django.utils import timezone

class CredentialService:
    @staticmethod
    def create_credential(property: int, ota: int, username: str, password: str) -> Credential:
        """
        Create a new credential for a given property and OTA profile.

        :param property_id: The property ID (ForeignKey to OTAProfile).
        :param ota_id: The OTA Profile ID (ForeignKey to PropertyProfile).
        :param username: The username for the credential.
        :param password: The password for the credential.
        :return: A new Credential instance.
        """
        try:
            property_profile = OTAProfile.objects.get(id=property)
            ota_profile = PropertyProfile.objects.get(id=ota)

            credential = Credential.objects.create(
                property=ota_profile,
                ota=property_profile,
                username=username,
                password=password,
                is_active=True  # Set default value for `is_active` as True
            )
            return credential
        except OTAProfile.DoesNotExist:
            raise ValueError(f"OTAProfile with id {property} not found.")
        except PropertyProfile.DoesNotExist:
            raise ValueError(f"PropertyProfile with id {ota} not found.")
        except IntegrityError as e:
            raise ValueError(f"Failed to create credential: {str(e)}")
    
    @staticmethod
    def update_credential(credential_id: int, username: str = None, password: str = None, is_active: bool = None) -> Credential:
        """
        Update an existing credential record.

        :param credential_id: The ID of the Credential to be updated.
        :param username: The new username (optional).
        :param password: The new password (optional).
        :param is_active: Whether the credential is active (optional).
        :return: The updated Credential instance.
        """
        try:
            credential = Credential.objects.get(id=credential_id)

            if username:
                credential.username = username
            if password:
                credential.password = password
            if is_active is not None:
                credential.is_active = is_active

            credential.save()
            return credential
        except Credential.DoesNotExist:
            raise ValueError(f"Credential with id {credential_id} not found.")
        except IntegrityError as e:
            raise ValueError(f"Failed to update credential: {str(e)}")

    @staticmethod
    def delete_credential(credential_id: int) -> bool:
        """
        Soft delete a credential by setting `deleted_at` timestamp.

        :param credential_id: The ID of the Credential to be deleted.
        :return: True if the credential was deleted, otherwise False.
        """
        try:
            credential = Credential.objects.get(id=credential_id)
            credential.deleted_at = timezone.now()
            credential.is_active = False  # Mark as inactive
            credential.save()
            return True
        except Credential.DoesNotExist:
            raise ValueError(f"Credential with id {credential_id} not found.")
    
    @staticmethod
    def get_active_credentials() -> list:
        """
        Get all active credentials.

        :return: A list of active Credential instances.
        """
        return Credential.objects.filter(is_active=True, deleted_at__isnull=True)

    @staticmethod
    def get_credential_by_user_and_property(username: str, property_id: int) -> Credential:
        """
        Get a specific credential by username and property ID.

        :param username: The username to search for.
        :param property_id: The property ID (ForeignKey to OTAProfile).
        :return: The matching Credential instance.
        """
        try:
            return Credential.objects.get(username=username, property_id=property_id, deleted_at__isnull=True)
        except Credential.DoesNotExist:
            raise ValueError(f"No credential found for username {username} and property ID {property_id}.")
        

    @staticmethod
    def get_all_credentials () :
        return Credential.objects.all()
