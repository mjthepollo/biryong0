from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from biryong.competition.models import Competition, Player, Setting


def home(request):
    setting = Setting.load()
    competitions = Competition.objects.all()
    return render(request, "home.html", context={"setting": setting, "competitions": competitions})


def get_real_time_info_json(request):
    real_time_competition = Competition.get_real_time_competition()
    if real_time_competition:
        return_json = {
            'name': real_time_competition.name,
            "time_string": real_time_competition.time_string,
            "match_url": reverse('competition:match', kwargs={'pk': real_time_competition.pk}),
            "join_match_fetch_url": reverse('competition:join_match_fetch',
                                            kwargs={'pk': real_time_competition.pk})
        }
    else:
        return_json = {
            "name": Setting.load().broad_cast_name,
            "time_string": "언제 끝날지 모름",
            "match_url": False,
            "join_match_fetch_url": False
        }
    return_json.update({"authenticated": request.user.is_authenticated})
    return JsonResponse(return_json)


def twitch_chat(request):
    return render(request, "twitch_chat.html")


def olympic_chat(request):
    return render(request, "olympic_chat.html")


def team2_chat(request):
    return render(request, "team2_chat.html")
