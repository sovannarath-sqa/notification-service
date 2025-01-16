from django.urls import path
from cookie_sessions.controllers.web_cookie_session_ctrl import CookieSessionView

urlpatterns = [
    path("start/", CookieSessionView.start_session, name="start_session"),
    path(
        "generate-sessions/",
        CookieSessionView.generate_sessions,
        name="generate_sessions",
    ),
    path(
        "fetch-profiles-sessions/",
        CookieSessionView.fetch_profiles,
        name="fetch_profile",
    ),
    # path(
    #     "get-session/",
    #     CookieSessionView.get_profile,
    #     name="get_profile",
    # ),
]
