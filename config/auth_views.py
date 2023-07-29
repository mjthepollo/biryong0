import requests
from django.conf import settings
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from biryong.users.forms import UserForm
from biryong.users.models import User

KAKAO_CLIENT_ID = settings.KAKAO_CLIENT_ID


def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    redirect_url = get_full_url_from_suffix(
        request, reverse('kakao:redirect'))
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CLIENT_ID}&redirect_uri={redirect_url}&response_type=code")


class KakaoLoginException(Exception):
    pass


def get_full_url_from_suffix(request, suffix):
    server_url = request._current_scheme_host
    return server_url + suffix


def get_access_token(request, callback_url):
    code = request.GET.get("code")
    CALLBACK_URL = get_full_url_from_suffix(request, callback_url)
    token_json = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_CLIENT_ID}&redirect_uri={CALLBACK_URL}&code={code}"
    ).json()
    error = token_json.get("error", None)
    if error:
        raise KakaoLoginException(error)
    else:
        return token_json.get("access_token")


def get_user_info(access_token):
    profile_json = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()
    kakao_account = profile_json.get("kakao_account")
    kakao_id = str(profile_json.get("id"))
    email = kakao_account.get("email", None)
    nickname = kakao_account["profile"]["nickname"]
    thumbnail_image_url = kakao_account["profile"]["thumbnail_image_url"]
    profile_image_url = kakao_account["profile"]["profile_image_url"]
    return {"kakao_id": kakao_id, "email": email, "nickname": nickname,
            "thumbnail_image_url": thumbnail_image_url, "profile_image_url": profile_image_url}


def kakao_redirect(request):
    try:
        access_token = get_access_token(
            request, reverse("kakao:redirect"))
        user_info = get_user_info(access_token)
    except KakaoLoginException:
        return redirect(reverse("login"))
    username = user_info["kakao_id"]
    email = user_info["email"]
    nickname = user_info["nickname"]
    profile_image_url = user_info["profile_image_url"]
    thumbnail_image_url = user_info["thumbnail_image_url"]
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.nickname = nickname
        user.profile_image_url = profile_image_url
        user.thumbnail_image_url = thumbnail_image_url
        user.save()
        login_user(request, user)
        return redirect("/")
    else:
        random_password = User.objects.make_random_password()
        user = User.objects.create_user(
            username=username, nickname=nickname,
            email=email, password=random_password,
            profile_image_url=profile_image_url, thumbnail_image_url=thumbnail_image_url)
        login_user(request, user)
        return redirect(reverse("home"))


@login_required
def logout(request):
    logout_user(request)
    return redirect(reverse("home"))
