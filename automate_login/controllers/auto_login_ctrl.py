from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import os
from decouple import config

from credential.dto.credential_dto import CredentialDTO
from automate_login.services.auto_login_service import AutoLoginService


@method_decorator(csrf_exempt, name="dispatch")
class AutomateLoginView(View):
    def post(self, request):
        """
        Handle POST requests for automated login and message sending.
        """
        try:
            if (
                not request.body.strip()
            ):  # Check if the body is empty or whitespace-only
                data = {}
                print(
                    "Empty or whitespace-only body received, defaulting to empty data."
                )
            else:
                try:
                    data = json.loads(request.body)
                    print("Parsed JSON data:", data)
                except json.JSONDecodeError:
                    return JsonResponse(
                        {"error": "Invalid JSON format or empty body."}, status=400
                    )

            # Extract parameters from environment variables
            username = config("PROPERTY_NAME", default=None)
            password = config("PROPERTY_PASSWORD", default=None)
            browser = config("PROPERTY_BROWSER", default="Firefox")
            channel = config("PROPERTY_CHANNEL", default=None)
            channel_id = config("PROPERTY_CHANNEL_ID", default=None)
            reservations = data.get("reservations", [])

            # Debug environment variables
            print(f"Environment variables: Username={username}, Channel={channel}")

            # Validate required environment variables
            if not all([username, password, channel]):
                return JsonResponse(
                    {
                        "error": "Missing required environment variables: PROPERTY_NAME, PROPERTY_PASSWORD, or PROPERTY_CHANNEL"
                    },
                    status=400,
                )

            # Create credential object
            credential = CredentialDTO(
                username=username,
                password=password,
                channel=channel,
                channel_id=channel_id,
                reservations=reservations,
            )

            # Handle login and automation
            if channel == "agoda":
                AutoLoginService.agoda_login(browser, credential, reservations)
            elif channel == "airbnb":
                AutoLoginService.airbnb_login(browser, credential, reservations)
            elif channel == "rakuten":
                AutoLoginService.rakuten_login(browser, credential, reservations)
            else:
                return JsonResponse({"error": "Unsupported channel"}, status=400)

            return JsonResponse(
                {"message": f"Login and message sending successful for {channel}"}
            )

        except Exception as e:
            print("Exception encountered:", str(e))
            return JsonResponse({"error": str(e)}, status=500)


# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework import viewsets
# from rest_framework.response import Response
# from credential.dto.credential_dto import CredentialDTO
# from automate_login.services.auto_login_service import AutoLoginService
# import json


# class AutomateLoginViewSet(viewsets.ViewSet):

#     def create(self, request, platform=None):
#         # Extracting data from the request body
#         data = json.loads(request.body)
#         username = data.get("username")
#         password = data.get("password")
#         channel_id = data.get("channel_id")
#         reservations = data.get("reservation_id")
#         channel_name = data.get("channel")
#         browser = data.get("browser")

#         # Validate required parameters
#         if not all([username, password, channel_name, channel_id, reservations]):
#             return Response(
#                 {"error": "Missing required parameters"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # Prepare the CredentialDTO object
#         credential = CredentialDTO(
#             username=username,
#             password=password,
#             channel_name=channel_name,
#             channel_id=channel_id,
#             reservations=reservations,
#         )

#         try:
#             # Based on platform, call the appropriate login service
#             if platform == "agoda":
#                 AutoLoginService.agoda_login(
#                     browser=browser, credential=credential, reservations=reservations
#                 )
#             elif platform == "airbnb":
#                 AutoLoginService.airbnb_login(browser=browser, credential=credential)
#             elif platform == "rakuten":
#                 AutoLoginService.rakuten_login(browser=browser, credential=credential)
#             else:
#                 return Response(
#                     {"error": "Unsupported platform"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             return Response({"message": "Login and message sending successful"})

#         except Exception as e:
#             return Response(
#                 {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
