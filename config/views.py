from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from biryong.competition.models import Competition, Player, Setting


def home(request):
    setting = Setting.load()
    return render(request, "home.html", context={"setting": setting})


def get_real_time_info_json(request):
    real_time_competition = Competition.get_real_time_competition()
    if real_time_competition:
        return_json = {'name': real_time_competition.name,
                       "time_string": real_time_competition.time_string}
    else:
        return_json = {"name": Setting.load().broad_cast_name, "time_string": "언제 끝날지 모름"}
    return JsonResponse(return_json)


def twitch_chat(request):
    return render(request, "twitch_chat.html")


def team1_chat(request):
    return render(request, "team1_chat.html")


def team2_chat(request):
    return render(request, "team2_chat.html")
