from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField, URLField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


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

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.
        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def __str__(self):
        return self.nickname
