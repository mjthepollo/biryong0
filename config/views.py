from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse


# @login_required
def home(request):
    return render(request, "pages/home.html")
    # return redirect(reverse("smalltalk:room", kwargs={"room_name": "lobby"}))