from django.urls import path
from one_password.controllers.one_password_ctrl import GetSecretView

urlpatterns = [
    path('secret/<str:secret_name>', GetSecretView.get_1password_secret, name='get-secret'),
]