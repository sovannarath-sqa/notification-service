from django.http import JsonResponse, HttpResponse
from credential.dto.credential_dto import CredentialDTO
from automate_login.services.auto_login_service import AutoLoginService
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json


class AutomateLoginView(View):

    @csrf_exempt
    def agoda_login_view(request):
        print("Agoda login view called")
        if request.method == "POST":
            data = json.loads(request.body)
            print("Received data:", data)
            username = data.get("username")
            password = data.get("password")
            channel_id = data.get("channel_id")
            reservations = data.get("reservations")
            channel = data.get("channel")
            browser = data.get("browser")

            # Print each variable to ensure correct data retrieval
            print("Username:", username)
            print("Password:", password)
            print("Channel ID:", channel_id)
            print("Reservations:", reservations)
            print("Channel Name:", channel)
            print("Browser:", browser)

            if not all([username, password, channel, channel_id, reservations]):
                print(
                    "Error: Missing required parameters"
                )  # Indicate a parameter is missing
                return JsonResponse(
                    {"error": "Missing required parameters"}, status=400
                )

            credential = CredentialDTO(
                username=username,
                password=password,
                channel=channel,
                channel_id=channel_id,
                reservations=reservations,
            )

            try:
                AutoLoginService.agoda_login(
                    browser=browser, credential=credential, reservations=reservations
                )
                return JsonResponse({"message": "Login and message sending successful"})

            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        return HttpResponse(status=405)

    @csrf_exempt
    def airbnb_login_view(request):
        print("Airbnb login view called")
        if request.method == "POST":
            data = json.loads(request.body)
            print(data)
            username = data.get("username")
            password = data.get("password")
            channel_id = data.get("channel_id")
            reservations = data.get("reservations")
            channel = data.get("channel")
            browser = data.get("browser")

            # Print each variable to ensure correct data retrieval
            print("Username:", username)
            print("Password:", password)
            print("Channel ID:", channel_id)
            print("Reservations:", reservations)
            print("Channel Name:", channel)
            print("Browser:", browser)

            if not all([username, password, channel, channel_id, reservations]):
                return JsonResponse(
                    {"error": "Missing required parameters"}, status=400
                )

            credential = CredentialDTO(
                username=username,
                password=password,
                channel=channel,
                channel_id=channel_id,
                reservations=reservations,
            )

            try:
                AutoLoginService.airbnb_login(
                    browser=browser, credential=credential, reservations=reservations
                )
                return JsonResponse({"message": "Login and message sending successful"})

            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        return HttpResponse(status=405)

    @csrf_exempt
    def rakuten_login_view(request):
        print("Rakuten login view called")
        if request.method == "POST":
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            channel_id = data.get("channel_id")
            reservations = data.get("reservation_id")
            channel = data.get("channel")
            browser = data.get("browser")

            if not all([username, password, channel, channel_id, reservations]):
                return JsonResponse(
                    {"error": "Missing required parameters"}, status=400
                )

            credential = CredentialDTO(
                username=username,
                password=password,
                channel=channel,
                channel_id=channel_id,
                reservations=reservations,
            )

            try:
                AutoLoginService.rakuten_login(browser=browser, credential=credential)
                return JsonResponse({"message": "Login and message sending successful"})

            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        return HttpResponse(status=405)


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
