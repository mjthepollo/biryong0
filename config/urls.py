from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from config.auth_views import login, logout
from config.views import get_real_time_info_json, home, team1_chat, team2_chat, twitch_chat

urlpatterns = [
    path("", home, name="home"),
    path("get_real_time_info_json/", get_real_time_info_json, name="get_real_time_info_json"),
    path("twitch_chat/", twitch_chat, name="twitch_chat"),

    path('team1_chat/', team1_chat, name='team1_chat'),
    path('team2_chat/', team2_chat, name='team2_chat'),
    path('twitch_chat/', twitch_chat, name='twitch_chat'),

    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("kakao/", include("config.auth_urls", namespace="kakao")),
    path("users/", include("biryong.users.urls", namespace="users")),

    path("smalltalk/", include("biryong.smalltalk.urls", namespace="smalltalk")),
    path("competition/", include("biryong.competition.urls", namespace="competition")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    re_path(r'^staticfiles/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
            }),
]  # TEMPROARY!!!!!

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
