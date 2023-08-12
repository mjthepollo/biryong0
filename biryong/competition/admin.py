from django.contrib import admin

from biryong.competition.models import Competition, Player, Setting

# Register your models here.


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('twitch', "youtube")


@admin.action(description="참가 불가능으로 만듦")
def make_unjoinable(modeladmin, request, queryset):
    queryset.update(joinable=False)


@admin.action(description="실시간으로 만듦")
def make_realtime(modeladmin, request, queryset):
    queryset.update(real_time=True)


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'joinable', 'real_time', "game_link", "discord_link")
    actions = [make_unjoinable, make_realtime]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'competition')
