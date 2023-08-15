from django.urls import path

from biryong.quiz.views import detail, quiz_list, quiz_list_info

app_name = "quiz"
urlpatterns = [
    path("", view=quiz_list, name="list"),
    path("detail/<int:pk>/", view=detail, name="detail"),
    path("info/", view=quiz_list_info, name="info"),
]
