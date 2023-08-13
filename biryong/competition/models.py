from django.db import models

# Create your models here.
from django.templatetags.static import static

from biryong.users.models import User
from config.models import TimeStampedModel


class Setting(models.Model):

    twitch = models.BooleanField(default=False)
    youtube = models.BooleanField(default=True)
    broad_cast_name = models.CharField(max_length=100, default="운동회가 망하지 않게 하기위해 무한 전화를 거는 김민준")

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Setting, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Competition(models.Model):
    class Meta:
        ordering = ['number']  # number에 대한 오른차숨

    name = models.CharField(default="경기명 설정이 필요합니다.", max_length=200, verbose_name="경기명")
    number = models.IntegerField(default=0)
    time_string = models.CharField(default="시간 설정이 필요합니다.", max_length=30)
    joinable = models.BooleanField(default=True, verbose_name="참가 가능")
    real_time = models.BooleanField(default=False, verbose_name="실시간")
    description = models.TextField(default="설명이 필요합니다.", verbose_name="설명")

    game_link = models.URLField(blank=True, null=True, verbose_name="게임 링크")
    discord_link = models.URLField(blank=True, null=True, verbose_name="디스코드 링크")

    @classmethod
    def get_real_time_competition(cls):
        return cls.objects.filter(real_time=True).first()

    @property
    def first_player(self):
        return self.active_players.first()

    @property
    def active_players(self):
        return self.players.filter(active=True)

    @property
    def number_of_active_players(self):
        return self.active_players.count()

    def pop_first_active_player(self):
        first_player = self.active_players.first()
        if first_player:
            first_player.active = False
            first_player.save()
        return first_player

    def __str__(self):
        return f"{self.name}"


class Player(TimeStampedModel):
    class Meta:
        ordering = ["created"]  # 첫번째가 가장 먼저 들어온 사람임
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE,
                                    verbose_name="경기", related_name="players", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="유저",
                             related_name="players", null=True, blank=True)

    active = models.BooleanField(default=True, verbose_name="활성화")

    def __str__(self):
        return f"{self.user}"
