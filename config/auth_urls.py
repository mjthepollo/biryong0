from django.urls import path

from config.auth_views import kakao_redirect

app_name = "users"
urlpatterns = [
    path("redirect/", view=kakao_redirect, name="redirect")
]
