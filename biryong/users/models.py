import random

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField, URLField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

COLOR_CHOICES = (
    ("#FF0000", "빨강"),
    ("#FCEE21", "노랑"),
    ("#39B54A", "초록"),
    ("#29ABE2", "파랑"),
    ("#000000", "검정"),

)


class User(AbstractUser):
    """
    Default custom user model for biryong.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    nickname = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), null=True, blank=True)

    kakao_id = CharField(max_length=50)
    profile_image_url = URLField(max_length=200, null=True, blank=True)
    thumbnail_image_url = URLField(max_length=200, null=True, blank=True)

    chat_name_color = CharField(max_length=10, choices=COLOR_CHOICES, default="#000000")

    join_quiz = models.BooleanField(default=False)
    solved_point = models.IntegerField(default=0)

    def set_solved_point(self):
        self.solved_point = sum([quiz.point for quiz in self.solved_quizs.all()])
        self.save()
        return self.solved_point

    def set_random_chat_name_color(self):
        self.chat_name_color = random.choice(COLOR_CHOICES)[0]
        self.save()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.
        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def __str__(self):
        return self.nickname
