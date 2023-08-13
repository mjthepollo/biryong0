# chat/urls.py
from django.urls import path

from biryong.competition.views import join_match_fetch, join_match_redirect, match, real_time

app_name = 'competition'

urlpatterns = [
    path("match/<int:pk>/", match, name="match"),
    path("join_match_fetch/<int:pk>/", join_match_fetch, name="join_match_fetch"),
    path("join_match_redirect/<int:pk>/", join_match_redirect, name="join_match_redirect"),
    path("real_time/", real_time, name="real_time"),
]
