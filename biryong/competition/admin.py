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


@admin.action(description="첫 선수를 제거함")
def pop_first_player(modeladmin, request, queryset):
    for competition in queryset:
        competition.pop_first_player()


class PlayerInline(admin.TabularInline):
    model = Player
    list_display = ('user', 'competition')


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'joinable', 'real_time',
                    "first_player", "number_of_players")
    actions = [make_unjoinable, make_realtime, pop_first_player]
    inlines = [PlayerInline]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'competition', "created")
