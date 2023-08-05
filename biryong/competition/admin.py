from django.contrib import admin

from biryong.competition.models import Competition, Player, Setting, Team

# Register your models here.


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('twitch', "youtube")


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('number', 'team1', 'team2', "open_expect_vote", 'finish_expect_vote',
                    "open_POG_vote", "finish_POG_vote", "pog_info")


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('team', 'name', 'nickname', "position", "tier")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', "number")
