from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from biryong.competition.models import Competition, Player, Setting


def home(request):
    setting = Setting.load()
    return render(request, "home.html", context={"setting": setting})


def set_banner(request):
    return_json = {'banner_href': reverse("home"), "banner_content": "배너 내용"}
    return JsonResponse(return_json)


def twitch_chat(request):
    return render(request, "twitch_chat.html")


def team1_chat(request):
    return render(request, "team1_chat.html")


def team2_chat(request):
    return render(request, "team2_chat.html")
