from django.http import JsonResponse
from django.views import View
from cookie_sessions.services.web_cookie_sessions import CookieSession
from django.views.decorators.csrf import csrf_exempt
import json


class CookieSessionView(View):

    @csrf_exempt
    def start_session(request):

        if request.method == "POST":
            data = json.loads(request.body)
            channel = data.get("channel")
            credential_name = data.get("credential_name")
            password = data.get("password")
            browser = data.get("browser")

            if not channel or not credential_name:
                return JsonResponse(
                    {
                        "error": "Missing required parameters: channel and credential_name"
                    },
                    status=400,
                )

            try:
                CookieSession.start_session(
                    browser=browser,
                    channel=channel,
                    credential_name=credential_name,
                    password=password,
                )
                return JsonResponse(
                    {
                        "message": f"Session started successfully for {channel} - {credential_name}"
                    },
                    status=200,
                )

            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse({"error": str(e)}, status=500)

    @csrf_exempt
    def get_cookies(request):
        """
        Endpoint to get cookies in JSON format.
        """
        if request.method == "POST":
            data = json.loads(request.body)
            channel = data.get("channel")
            credential_name = data.get("credential_name")

            if not channel or not credential_name:
                return JsonResponse(
                    {
                        "error": "Missing required parameters: channel and credential_name"
                    },
                    status=400,
                )

            try:
                cookies = CookieSession.get_cookies_as_json(
                    channel=channel, credential_name=credential_name
                )
                return JsonResponse({"cookies": cookies}, status=200)
            except FileNotFoundError as e:
                return JsonResponse({"error": str(e)}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse(
                {"error": "Invalid request method. Only POST is allowed."}, status=405
            )
