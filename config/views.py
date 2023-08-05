from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from biryong.competition.models import Competition, Player, Setting, Team
from biryong.users.forms import AdditionalInfoForm


def home(request):
    setting = Setting.load()
    return render(request, "home.html", context={"setting": setting})


@login_required
def team_supporters(request, number):
    team = Team.objects.get(number=number)
    return render(request, "team_supporters.html", context={"supporters": team.supporters.all(), "class": f"team{team.number}"})


@login_required
def expect_winner(request, competition_pk):
    competition = Competition.objects.get(pk=competition_pk)
    if competition.open_expect_vote:
        team1_expectors_count = competition.get_team1_expectors_count()
        team2_expectors_count = competition.get_team2_expectors_count()
        if team1_expectors_count + team2_expectors_count == 0:
            team1_expectors_rate = 50
            team2_expectors_rate = 50
        else:
            team1_expectors_rate = int(team1_expectors_count / (team1_expectors_count + team2_expectors_count) * 100)
            team2_expectors_rate = int(team2_expectors_count / (team1_expectors_count + team2_expectors_count) * 100)

        return render(request, "expect_winner.html",
                      context={"competition": competition,
                               "team1_expectors_count": team1_expectors_count,
                               "team2_expectors_count": team2_expectors_count,
                               "team1_expectors_rate": team1_expectors_rate,
                               "team2_expectors_rate": team2_expectors_rate,
                               })
    else:
        return redirect("home")


def vote_expected_winner(request, competition_pk, team_pk):
    competition = Competition.objects.get(pk=competition_pk)
    team = Team.objects.get(pk=team_pk)
    setattr(request.user, f"competition{competition.number}_winner_expect", team)
    request.user.save()
    return redirect(reverse("expect_winner", args=[competition_pk]))


@login_required
def vote_POG(request, competition_pk):
    competition = Competition.objects.get(pk=competition_pk)
    POG_of_user = request.user.competition1_POG
    if competition.open_POG_vote:
        return render(request, "vote_POG.html", {"competition": competition, "POG_of_user": POG_of_user})
    else:
        return redirect("home")


def vote_POG_player(request, competition_pk, player_pk):
    competition = Competition.objects.get(pk=competition_pk)
    player = Player.objects.get(pk=player_pk)
    pog_voters = getattr(player, f"competition{competition.number}_POG_voters")
    pog_voters.add(request.user)
    return redirect(reverse("vote_POG", args=[competition_pk]))


@login_required
def vote_MVP_and_MEP(request):
    team1 = Team.get_team1()
    team2 = Team.get_team2()
    MVP_of_user = request.user.MVP
    MEP_of_user = request.user.MEP
    team1_players = team1.players_in_order()
    team2_players = team2.players_in_order()
    all_players = []
    for i in range(5):
        all_players.append(team1_players[i])
        all_players.append(team2_players[i])
    return render(request, "vote_MVP_and_MEP.html",
                  {"team1": team1, "team2": team2,
                   "all_players": all_players,
                   "MVP_of_user": MVP_of_user,
                   "MEP_of_user": MEP_of_user})


@login_required
def vote_MVP_player(request, player_pk):
    player = Player.objects.get(pk=player_pk)
    request.user.MVP = player
    request.user.save()
    return redirect(reverse("vote_MVP_and_MEP"))


@login_required
def vote_MEP_player(request, player_pk):
    player = Player.objects.get(pk=player_pk)
    request.user.MEP = player
    request.user.save()
    return redirect(reverse("vote_MVP_and_MEP"))


@login_required
def set_additional_info(request):
    if request.method == "GET":
        additional_info_form = AdditionalInfoForm(instance=request.user)
        return render(request, "set_additional_info.html", context={"additional_info_form": additional_info_form})
    else:
        additional_info_form = AdditionalInfoForm(request.POST, instance=request.user)
        if additional_info_form.is_valid():
            additional_info_form.save()
            request.user.info_complete = True
            request.user.save()
            return redirect(reverse("home"))
        else:
            raise Exception("폼이 유효하지 않습니다.")


def twitch_chat(request):
    return render(request, "twitch_chat.html")


def get_expect_winner_url(request):
    competition1 = Competition.objects.get(number=1)
    competition2 = Competition.objects.get(number=2)
    competition3 = Competition.objects.get(number=3)
    if competition1.open_expect_vote and not competition1.finish_expect_vote:
        return_json = {'inner_html': '1경기 승자예측', 'href': reverse(
            "expect_winner", args=[competition1.pk]), 'active': True}
    elif competition1.open_expect_vote and competition1.finish_expect_vote and not competition2.open_expect_vote:
        return_json = {'inner_html': '1경기 승자예측', 'href': "", 'active': False}
    elif competition2.open_expect_vote and not competition2.finish_expect_vote:
        return_json = {'inner_html': '2경기 승자예측', 'href': reverse(
            "expect_winner", args=[competition1.pk]), 'active': True}
    elif competition2.open_expect_vote and competition2.finish_expect_vote and not competition3.open_expect_vote:
        return_json = {'inner_html': '2경기 승자예측', 'href': "", 'active': False}
    elif competition3.open_expect_vote and not competition3.finish_expect_vote:
        return_json = {'inner_html': '3경기 승자예측', 'href': reverse(
            "expect_winner", args=[competition3.pk]), 'active': True}
    else:
        return_json = {'inner_html': 'MVP/MEP 투표',
                       'href': reverse("vote_MVP_and_MEP"), 'active': True}
    return JsonResponse(return_json)


def get_vote_POG_url(request):
    competition1 = Competition.objects.get(number=1)
    competition2 = Competition.objects.get(number=2)
    competition3 = Competition.objects.get(number=3)
    if not competition1.open_POG_vote and not competition1.finish_POG_vote:
        return_json = {'inner_html': '1경기 POG 투표', 'href': reverse(
            "vote_POG", args=[competition1.pk]), 'active': False}
    elif competition1.open_POG_vote and not competition1.finish_POG_vote:
        return_json = {'inner_html': '1경기 POG 투표', 'href': reverse(
            "vote_POG", args=[competition1.pk]), 'active': True}
    elif competition1.open_POG_vote and competition1.finish_POG_vote and not competition2.open_POG_vote:
        return_json = {'inner_html': '1경기 POG 투표', 'href': "", 'active': False}
    elif competition2.open_POG_vote and not competition2.finish_POG_vote:
        return_json = {'inner_html': '2경기 POG 투표', 'href': reverse(
            "vote_POG", args=[competition1.pk]), 'active': True}
    elif competition2.open_POG_vote and competition2.finish_POG_vote and not competition3.open_POG_vote:
        return_json = {'inner_html': '2경기 POG 투표', 'href': "", 'active': False}
    elif competition3.open_POG_vote and not competition3.finish_POG_vote:
        return_json = {'inner_html': '3경기 POG 투표', 'href': reverse(
            "vote_POG", args=[competition3.pk]), 'active': True}
    elif competition3.open_POG_vote and competition3.finish_POG_vote:
        return_json = {'inner_html': '3경기 POG 투표', 'href': "", 'active': False}
    else:
        return_json = {'inner_html': '3경기 POG 투표', 'href': "", 'active': False}
    return JsonResponse(return_json)


def team1_chat(request):
    return render(request, "team1_chat.html")


def team2_chat(request):
    return render(request, "team2_chat.html")
