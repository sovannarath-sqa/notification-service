from django.urls import path
from automate_login.controllers.auto_login_ctrl import AutomateLoginView

urlpatterns = [
    path(
        "agoda-automate-message",
        AutomateLoginView.agoda_login_view,
        name="agoda-automate-message",
    ),
    path(
        "airbnb-automate-message",
        AutomateLoginView.airbnb_login_view,
        name="airbnb-automate-message",
    ),
    path(
        "rakuten-automate-message",
        AutomateLoginView.rakuten_login_view,
        name="rakuten-automate-message",
    ),
]
