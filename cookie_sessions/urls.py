from django.urls import path
from cookie_sessions.controllers.web_cookie_session_ctrl import CookieSessionView

urlpatterns = [
    path("start", CookieSessionView.start_session, name="start_session"),
    path("get-cookies/", CookieSessionView.get_cookies, name="get_cookies"),
    path(
        "download-cookies/",
        CookieSessionView.download_cookies_as_file,
        name="download_cookies",
    ),
    path(
        "genearete-session/",
        CookieSessionView.generate_session,
        name="generate_session",
    ),
    path(
        "get-session/",
        CookieSessionView.get_profile,
        name="get_profile",
    ),
]
