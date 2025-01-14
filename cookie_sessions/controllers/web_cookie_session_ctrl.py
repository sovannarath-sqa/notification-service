from django.http import JsonResponse, HttpResponse
from django.views import View
from cookie_sessions.services.web_cookie_sessions import CookieSession
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


def parse_request_body(request):
    try:
        return json.loads(request.body), None
    except json.JSONDecodeError as e:
        return None, {"error": "Invalid JSON body.", "details": str(e)}


@method_decorator(csrf_exempt, name="dispatch")
class CookieSessionView(View):

    @require_http_methods(["POST"])
    def start_session(request):
        data, error = parse_request_body(request)
        if error:
            return JsonResponse(error, status=400)

        channel = data.get("channel")
        credential_name = data.get("credential_name")
        password = data.get("password")
        browser = data.get("browser")

        if not channel or not credential_name:
            return JsonResponse(
                {"error": "Missing required parameters: channel and credential_name"},
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

    @require_http_methods(["POST"])
    def get_cookies(request):
        data, error = parse_request_body(request)
        if error:
            return JsonResponse(error, status=400)

        channel = data.get("channel")
        credential_name = data.get("credential_name")

        if not channel or not credential_name:
            return JsonResponse(
                {"error": "Missing required parameters: channel and credential_name"},
                status=400,
            )

        try:
            cookies = CookieSession.get_cookies_as_json(
                channel=channel, credential_name=credential_name
            )
            return JsonResponse(cookies, status=200)
        except FileNotFoundError as e:
            return JsonResponse({"error": str(e)}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @csrf_exempt
    @require_http_methods(["POST"])
    def generate_sessions(request):
        try:
            session_details = CookieSession.generate_sessions()
            return JsonResponse(
                {
                    "message": "Sessions generated successfully.",
                    "details": session_details,
                },
                status=200,
            )
        except FileNotFoundError as fnfe:
            return JsonResponse({"error": str(fnfe)}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @require_http_methods(["GET"])
    def fetch_profiles(request):
        try:
            profiles = CookieSession.fetch_profile_sessions()
            return JsonResponse(profiles, status=200)
        except FileNotFoundError as fnfe:
            return JsonResponse({"error": str(fnfe)}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
