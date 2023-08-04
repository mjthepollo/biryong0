from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from biryong.competition.models import Competition, Player, Team


def home(request):
    return render(request, "home.html")


@login_required
def team_supporters(request, pk):
    team = Team.objects.get(pk=pk)
    return render(request, "team_supporters.html", {"supporters": team.supporters.all()})


@login_required
def expect_winner(request, competition_pk):
    competition = Competition.objects.get(pk=competition_pk)
    return render(request, "expect_winner.html", {"competition": competition})


def vote_expected_winner(request, competition_pk, team_pk):
    competition = Competition.objects.get(pk=competition_pk)
    team = Team.objects.get(pk=team_pk)
    if team == competition.team1:
        competition.team1_expector.add(request.user)
        return JsonResponse({'result': 'success', 'meesage': f"{request.user.nickname}님이 {team.name}을 응원합니다."})
    elif team == competition.team2:
        competition.team2_expector.add(request.user)
        return JsonResponse({'result': 'success', 'meesage': f"{request.user.nickname}님이 {team.name}을 응원합니다."})
    else:
        return JsonResponse({'result': 'fail', "message": "팀이 올바르지 않습니다."})


@login_required
def vote_POG(request, competition_pk):
    competition = Competition.objects.get(pk=competition_pk)
    POG_of_user = request.user.competition1_POG
    return render(request, "select_POG.html", {"competition": competition, "POG_of_user": POG_of_user})


def vote_POG_player(request, competition_pk, player_pk):
    try:
        competition = Competition.objects.get(pk=competition_pk)
        player = Player.objects.get(pk=player_pk)
        pog_voters = getattr(player, f"competition{competition.number}_POG_voters")
        pog_voters.add(request.user)
        return JsonResponse({'result': 'success',
                             'meesage': f"{request.user.nickname}님이 {str(player.name)}님을 POG로 선택하셨습니다."})
    except Exception as e:
        return JsonResponse({'result': 'fail', 'meesage': f"{e}"})


@login_required
def vote_MVP_and_MEP(request):
    team1 = Team.objects.all()[0]
    team2 = Team.objects.all()[1]
    MVP_of_user = request.user.MVP
    MEP_of_user = request.user.MVP
    return render(request, "vote_MVP_and_MEP.html",
                  {"team1": team1, "team2": team2, "MVP_of_user": MVP_of_user,
                   "MEP_of_user": MEP_of_user})


@login_required
def vote_MVP_player(request, player_pk):
    try:
        player = Player.objects.get(pk=player_pk)
        MVP_voters = player.MVP_voters
        MVP_voters.add(request.user)
        return JsonResponse({'result': 'success',
                             'meesage': f"{request.user.nickname}님이 {str(player.name)}님을 MVP로 선택하셨습니다."})
    except Exception as e:
        return JsonResponse({'result': 'fail', 'meesage': f"{e}"})


@login_required
def vote_MEP_player(request, player_pk):
    try:
        player = Player.objects.get(pk=player_pk)
        MEP_voters = player.MEP_voters
        MEP_voters.add(request.user)
        return JsonResponse({'result': 'success',
                             'meesage': f"{request.user.nickname}님이 {str(player.name)}님을 MEP로 선택하셨습니다."})
    except Exception as e:
        return JsonResponse({'result': 'fail', 'meesage': f"{e}"})


@login_required
def twitch_set(request):
    return render(request, "twitch_set.html")


def twitch_chat(request):
    return render(request, "twitch_chat.html")
