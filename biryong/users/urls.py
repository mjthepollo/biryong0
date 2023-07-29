from django.urls import path

from biryong.users.views import user_detail_view

app_name = "users"
urlpatterns = [
    path("<int:pk>/", view=user_detail_view, name="detail"),
]
