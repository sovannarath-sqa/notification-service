from django.db import IntegrityError
from credential.models.propertyprofile import PropertyProfile
from django.utils.timezone import now


class PropertyProfileService:

    @staticmethod
    def create_property_profile(
        name,
        logo,
        suitebook_id,
        aos_slug,
        aos_organization_name,
        aos_organization_slug,
        description,
    ):
        """
        Create a new PropertyProfile instance.
        """
        try:
            property_profile = PropertyProfile.objects.create(
                name=name,
                logo=logo,
                suitebook_id=suitebook_id,
                aos_slug=aos_slug,
                aos_organization_name=aos_organization_name,
                aos_organization_slug=aos_organization_slug,
                description=description,
            )
            return property_profile
        except IntegrityError as e:
            # Handle any database-related errors
            return {"error": str(e)}

    @staticmethod
    def update_property_profile(
        property_profile_id,
        name,
        logo,
        suitebook_id,
        aos_slug,
        aos_organization_name,
        aos_organization_slug,
        description,
    ):

        if aos_slug:
            # Check if there's already a property profile with the same aos_slug, excluding the current one
            existing_profile = (
                PropertyProfile.objects.exclude(id=property_profile_id)
                .filter(aos_slug=aos_slug)
                .first()
            )
            if existing_profile:
                return {
                    "error": "The aos_slug is already in use. Please choose a different one."
                }
        print(
            f"Updating PropertyProfile {property_profile_id} with values: name={name}, suitebook_id={suitebook_id}, aos_slug={aos_slug}"
        )
        """
        Update an existing PropertyProfile instance by ID.
        """
        print(
            f"Attempting to update PropertyProfile with ID: {property_profile_id}"
        )  # Debugging ID lookup

        try:
            property_profile = PropertyProfile.objects.get(id=property_profile_id)
            print(
                f"Found PropertyProfile: {property_profile}"
            )  # Debugging the object found

            # Update only fields that are provided
            print(
                f"Received update request for PropertyProfile ID {property_profile_id} with data: "
                f"name={name}, suitebook_id={suitebook_id}, aos_slug={aos_slug}, "
                f"aos_organization_name={aos_organization_name}, aos_organization_slug={aos_organization_slug}, "
                f"description={description}"
            )

            if name not in [None, ""]:
                print(f"Updating name to: {name}")  # Check for empty string as well
                property_profile.name = name

                property_profile.name = name
            if logo is not None:
                print(f"Updating logo to: {logo}")  # Debugging logo change
                property_profile.logo = logo
            if suitebook_id is not None:
                print(
                    f"Updating suitebook_id to: {suitebook_id}"
                )  # Debugging suitebook_id change
                property_profile.suitebook_id = suitebook_id
            if aos_slug is not None:
                print(f"Updating aos_slug to: {aos_slug}")  # Debugging aos_slug change
                property_profile.aos_slug = aos_slug
            if aos_organization_name is not None:
                print(
                    f"Updating aos_organization_name to: {aos_organization_name}"
                )  # Debugging aos_organization_name change
                property_profile.aos_organization_name = aos_organization_name
            if aos_organization_slug is not None:
                print(
                    f"Updating aos_organization_slug to: {aos_organization_slug}"
                )  # Debugging aos_organization_slug change
                property_profile.aos_organization_slug = aos_organization_slug
            if description is not None:
                print(
                    f"Updating description to: {description}"
                )  # Debugging description change
                property_profile.description = description

                print(f"PropertyProfile before saving: {property_profile}")
                property_profile.save()
                print(f"PropertyProfile after saving: {property_profile}")

            return property_profile
        except PropertyProfile.DoesNotExist:
            print(
                f"PropertyProfile with ID {property_profile_id} not found."
            )  # Debugging not found error
            return {"error": "PropertyProfile not found"}, 404
        except IntegrityError as e:
            print(
                f"IntegrityError in update_property_profile: {str(e)}"
            )  # Debugging error
            return {"error": f"IntegrityError: {str(e)}"}, 400
        except Exception as e:
            print(
                f"Unexpected error in update_property_profile: {str(e)}"
            )  # Debugging general error
            return {"error": f"Unexpected error: {str(e)}"}, 500

    @staticmethod
    def delete_property_profile(property_profile_id):
        """
        Soft delete a PropertyProfile instance (set the deleted_at timestamp).
        """
        try:
            property_profile = PropertyProfile.objects.get(id=property_profile_id)
            property_profile.deleted_at = (
                now()
            )  # Soft delete the object by setting the deleted_at field
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
        return PropertyProfile.objects.filter(deleted_at__isnull=True).order_by(
            "-created_at"
        )
