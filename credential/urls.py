from django.urls import path
from credential.controllers.ota_profile_ctrl import  OTAProfileView
from credential.controllers.property_profile_ctrl import PropertyProfileView
from credential.controllers.credential_ctrl import CredentialView

urlpatterns = [
    # OTA Profile Endpoint
    path('ota-profiles/',  OTAProfileView.get_all_ota_profiles, name='get_all_ota_profiles'),
    path('ota-profiles/create/', OTAProfileView.create_ota_profile, name='create_ota_profile'),
    path('ota-profiles/<int:profile_id>/', OTAProfileView.get_ota_profile, name='get_ota_profile'),
    path('ota-profiles/<int:profile_id>/update/', OTAProfileView.update_ota_profile, name='update_ota_profile'),
    path('ota-profiles/<int:profile_id>/delete/', OTAProfileView.delete_ota_profile, name='delete_ota_profile'),
    path('ota-profiles/<int:profile_id>/restore/', OTAProfileView.restore_ota_profile, name='restore_ota_profile'),

    # Property Endpoint
    path('property-profiles/', PropertyProfileView.get_all_properties, name='property-profile-list'),
    path('property-profile/<int:property_profile_id>/', PropertyProfileView.get_property_detail, name='property-profile-detail'),
    path('property-profile/create/', PropertyProfileView.create_property, name='property-profile-create'),
    path('property-profile/update/<int:property_profile_id>/', PropertyProfileView.update_property, name='property-profile-update'),
    path('property-profile/delete/<int:property_profile_id>/', PropertyProfileView.delete_property, name='property-profile-delete'),

    # Credetial Endpoint
    path('credentials/create', CredentialView.create_credential, name='create-credential'),
    path('credentials/<int:credential_id>/', CredentialView.update_credential, name='update-credential'),
    path('credentials/<int:credential_id>/delete/', CredentialView.delete_credential, name='delete-credential'),
    path('credentials/active/', CredentialView.get_credential_detail, name='get-active-credentials'),
    path('credentials/', CredentialView.get_all_credentials, name='get-all-credentials')
]
