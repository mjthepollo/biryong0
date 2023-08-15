from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from biryong.quiz.models import Quiz
from biryong.users.models import User


@login_required
def quiz_list(request):
    user = request.user
    if not user.is_staff:
        user.join_quiz = True
        user.save()
    quizs = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', context={"quizs": quizs})


@staff_member_required
def detail(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quiz/detail.html', context={"quiz": quiz})


@login_required
def point_info(request):
    joined_users = User.objects.filter(join_quiz=True).order_by('solved_point')
    users_info = [{"thumbnail_image_url": user.thumbnail_image_url, "nickname": user.nickname, "solved_point": user.solved_point}
                  for user in joined_users]
    json = {"users_info": users_info}
    return JsonResponse(json)


@login_required
def solved_quizs(request):
    solved_quiz_list = Quiz.objects.filter(solved=True)
    json = {"solved_quiz_list": [{"quiz_pk": quiz.pk} for quiz in solved_quiz_list]}
    return JsonResponse(json)


@staff_member_required
def give_point(request, pk):
    return render(request, 'give_point.html')
