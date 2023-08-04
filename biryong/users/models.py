from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField, URLField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from biryong.competition.models import Player, Team


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

    support_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="supporters")
    cheer_message = models.TextField(blank=True, null=True)
    twitch_id = models.CharField(max_length=50, blank=True, null=True)
    info_complete = models.BooleanField(default=False)

    competition1_winner_expect = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True,
                                                   blank=True, related_name="competition1_expectors")
    competition2_winner_expect = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True,
                                                   blank=True, related_name="competition2_expectors")
    competition3_winner_expect = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True,
                                                   blank=True, related_name="competition3_expectors")

    competition1_POG = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True,
                                         blank=True, related_name="competition1_POG_voters")
    competition2_POG = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True,
                                         blank=True, related_name="competition2_POG_voters")
    competition3_POG = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True,
                                         blank=True, related_name="competition3_POG_voters")
    MVP = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True,
                            blank=True, related_name="MVP_voters")
    MEP = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True,
                            blank=True, related_name="MEP_voters")

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.
        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def is_team1_supporter(self):
        return self.support_team == Team.objects.get(number=1)

    def is_team2_supporter(self):
        return self.support_team == Team.objects.get(number=2)
