from django.db import models

# Create your models here.
from django.templatetags.static import static

POSITION_CHOICES = (
    ("bottom", "원딜"),
    ("jungle", "정글"),
    ("mid", "미드"),
    ("top", "탑"),
    ("supporter", "서폿"),
)


class Team(models.Model):
    name = models.CharField(max_length=30)

    @property
    def bottom(self):
        return self.players.get(position="bottom")

    @property
    def jungle(self):
        return self.players.get(position="jungle")

    @property
    def mid(self):
        return self.players.get(position="mid")

    @property
    def top(self):
        return self.players.get(position="top")

    @property
    def supporter(self):
        return self.players.get(position="supporter")


TIER_CHOICES = (
    ("bronze", "브론즈"),
    ("silver", "실버"),
    ("gold", "골드"),
    ("platinum", "플래티넘"),
    ("emerald", "에메랄드"),
    ("diamond", "다이아"),
    ("master", "마스터"),
    ("grand_master", "그마"),
)


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=100)
    position = models.CharField(max_length=30, choices=POSITION_CHOICES)
    tier = models.CharField(max_length=30, choices=TIER_CHOICES)

    @property
    def position_image_url(self):
        if self.position == 'bottom':
            return static('images/position/bottom.webp')
        elif self.position == 'jungle':
            return static('images/position/jungle.svg')
        elif self.position == 'mid':
            return static('images/position/mid.svg')
        elif self.position == 'top':
            return static('images/position/top.svg')
        elif self.position == 'supporter':
            return static('images/position/supporter.svg')
        else:
            return "ERROR"

    @property
    def tier_image_url(self):
        if self.tier == 'bronze':
            return static('images/tier/bronze.webp')
        elif self.tier == 'silver':
            return static('images/tier/silver.webp')
        elif self.tier == 'gold':
            return static('images/tier/gold.webp')
        elif self.tier == 'platinum':
            return static('images/tier/platinum.webp')
        elif self.tier == 'emerald':
            return static('images/tier/emerald.png')
        elif self.tier == 'diamond':
            return static('images/tier/diamond.webp')
        elif self.tier == 'master':
            return static('images/tier/master.webp')
        elif self.tier == 'grand_master':
            return static('images/tier/grand_master.webp')
        else:
            return "ERROR"


class Competition(models.Model):
    number = models.IntegerField(default=0)
    team1 = models.ForeignKey(Team,
                              on_delete=models.SET_NULL, null=True,
                              blank=True, related_name="team1")
    team2 = models.ForeignKey(Team,
                              on_delete=models.SET_NULL, null=True,
                              blank=True, related_name="team2")

    open_POG_vote = models.BooleanField(default=False)
    finish_POG_vote = models.BooleanField(default=False)

    open_expect_vote = models.BooleanField(default=False)
    finish_expect_vote = models.BooleanField(default=False)

    @property
    def pog_info(self):
        pog_votes_info = [(getattr(player, f"competition{self.index}_POG_voters").count(),
                           f"{player.name}/{player.nickname}") for player in self.team1.players.all()]
        pog_votes_info += [(getattr(player, f"competition{self.index}_POG_voters").count(),
                            f"{player.name}/{player.nickname}") for player in self.team2.players.all()]
        pog_votes_info.sort(key=lambda x: x[0], reverse=True)
        return str((pog_votes_info[:3]))

    def __str__(self):
        return f"[{self.team1.name} vs {self.team2.name}] {self.index}경기"
