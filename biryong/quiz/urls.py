from django.urls import path

from biryong.quiz.views import detail, give_point, point_info, quiz_list

app_name = "quiz"
urlpatterns = [
    path("", view=quiz_list, name="list"),
    path("detail/<int:pk>/", view=detail, name="detail"),
    path("point_info/", view=point_info, name="point_info"),
    path("give_point/<int:pk>/", view=give_point, name="give_point"),
]
