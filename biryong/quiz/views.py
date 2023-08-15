from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from biryong.quiz.forms import SolveForm
from biryong.quiz.models import Quiz
from biryong.users.models import User


def get_quiz_info():
    top3_players = User.objects.filter(join_quiz=True).order_by('-solved_point')[:3]
    top3_players_info = [{
        "thumbnail_image_url": player.thumbnail_image_url,
        "nickname": player.nickname,
        "solved_point": player.solved_point
    } for player in top3_players]

    other_players = User.objects.filter(join_quiz=True).order_by('-solved_point')[3:]
    other_players_info = [{
        "thumbnail_image_url": player.thumbnail_image_url,
        "nickname": player.nickname,
        "solved_point": player.solved_point
    } for player in other_players]

    solved_quizs = Quiz.objects.filter(solved=True)
    solved_quizs_pk = [quiz.pk for quiz in solved_quizs]
    quizs = Quiz.objects.all().order_by('pk')
    quiz_info = {
        "quizs": quizs,
        "top3_players_info": top3_players_info,
        "other_players_info": other_players_info,
        "solved_quizs_pk": solved_quizs_pk
    }
    return quiz_info


@login_required
def quiz_list(request):
    quiz_info = get_quiz_info()
    return render(request, 'quiz.html', context=quiz_info)


@login_required
def quiz_list_info(request):
    quiz_info = get_quiz_info()
    quiz_info.pop("quizs")
    return JsonResponse(quiz_info)


@staff_member_required
def detail(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    if request.method == "GET":
        solve_form = SolveForm(instance=quiz)
        return render(request, 'quiz_detail.html', context={"quiz": quiz, "solve_form": solve_form})
    elif request.method == "POST":
        solve_form = SolveForm(request.POST, instance=quiz)
        if solve_form.is_valid():
            solve_form.save()
            quiz.solved = True
            quiz.save()
        return render(request, 'quiz_detail.html', context={"quiz": quiz, "solve_form": solve_form})
