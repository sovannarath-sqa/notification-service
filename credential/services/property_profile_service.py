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
            existing_profile = (
                PropertyProfile.objects.exclude(id=property_profile_id)
                .filter(aos_slug=aos_slug)
                .first()
            )
            if existing_profile:
                return {
                    "error": "The aos_slug is already in use. Please choose a different one."
                }

        try:
            property_profile = PropertyProfile.objects.get(id=property_profile_id)

            if name not in [None, ""]:
                property_profile.name = name
            if logo is not None:
                property_profile.logo = logo
            if suitebook_id is not None:
                property_profile.suitebook_id = suitebook_id
            if aos_slug is not None:
                property_profile.aos_slug = aos_slug
            if aos_organization_name is not None:
                property_profile.aos_organization_name = aos_organization_name
            if aos_organization_slug is not None:
                property_profile.aos_organization_slug = aos_organization_slug
            if description is not None:
                property_profile.description = description

                property_profile.save()

            return property_profile
        except PropertyProfile.DoesNotExist:
            return {"error": "PropertyProfile not found"}, 404
        except IntegrityError as e:
            return {"error": f"IntegrityError: {str(e)}"}, 400
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

    @staticmethod
    def delete_property_profile(property_profile_id):
        try:
            property_profile = PropertyProfile.objects.get(id=property_profile_id)
            property_profile.deleted_at = now()
            property_profile.save()
            return property_profile
        except PropertyProfile.DoesNotExist:
            return {"error": "PropertyProfile not found"}

    @staticmethod
    def get_property_profile(property_profile_id):
        try:
            property_profile = PropertyProfile.objects.get(id=property_profile_id)
            return property_profile
        except PropertyProfile.DoesNotExist:
            return {"error": "PropertyProfile not found"}

    @staticmethod
    def get_all_property_profiles():
        return PropertyProfile.objects.filter(deleted_at__isnull=True).order_by(
            "-created_at"
        )
