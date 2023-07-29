from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from biryong.users.models import User


@login_required
def user_detail_view(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, "users/user_detail.html", {"user": user})
