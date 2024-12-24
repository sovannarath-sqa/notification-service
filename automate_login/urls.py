# from django.urls import path
# from automate_login.controllers.auto_login_ctrl import AutomateLoginView

# urlpatterns = [
#     path(
#         "agoda-automate-message",
#         AutomateLoginView.agoda_login_view,
#         name="agoda-automate-message",
#     ),
#     path(
#         "airbnb-automate-message",
#         AutomateLoginView.airbnb_login_view,
#         name="airbnb-automate-message",
#     ),
#     path(
#         "rakuten-automate-message",
#         AutomateLoginView.rakuten_login_view,
#         name="rakuten-automate-message",
#     ),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from automate_login.controllers.auto_login_ctrl import AutomateLoginViewSet

# Initialize the router
router = DefaultRouter()

# Register the AutomateLoginViewSet with the router
router.register(r"automate-login", AutomateLoginViewSet, basename="automate-login")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "automate-login/<str:platform>/",
        AutomateLoginViewSet.as_view(),
        name="automate-login-platform",
    ),
]
