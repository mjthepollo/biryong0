from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from biryong.competition.models import Competition, Player, Setting


def real_time(request):
    setting = Setting.load()
    real_time_competition = Competition.get_real_time_competition()
    return render(request, 'real_time.html', context={'setting': setting, 'real_time_competition': real_time_competition})


def match(request, pk):
    competition = Competition.objects.get(pk=pk)
    return render(request, 'match.html', context={'competition': competition})


@login_required
def join_match_redirect(request, pk):
    user = request.user
    competition = Competition.objects.get(pk=pk)
    if not Player.objects.filter(user=user, competition=competition, active=True).exists():
        Player.objects.create(user=user, competition=competition, active=True)
    return redirect(reverse('competition:match', kwargs={'pk': pk}))


@login_required
def join_match_fetch(request, pk):
    try:
        user = request.user
        competition = Competition.objects.get(pk=pk)
        if not Player.objects.filter(user=user, competition=competition, active=True).exists():
            Player.objects.create(user=user, competition=competition, active=True)
            return JsonResponse({'success': True, "message": "참가 완료"})
        else:
            return JsonResponse({'success': True, "message": "이미 있음"})
    except Exception as e:
        return JsonResponse({'success': False, "message": str(e)})
