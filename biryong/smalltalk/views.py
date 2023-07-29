from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, "smalltalk/index.html")


@login_required
def room(request, room_name):
    return render(request, "smalltalk/room.html", {"room_name": room_name})
