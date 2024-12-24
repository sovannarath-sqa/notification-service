from django.urls import path
from one_password.controllers.one_password_ctrl import GetSecretView

urlpatterns = [
    path('list', GetSecretView.get_item_list, name='get-list'),
    path('secret', GetSecretView.get_item_secret, name='get-secret'),
]