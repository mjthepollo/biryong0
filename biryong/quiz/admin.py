from django.contrib import admin

from biryong.quiz.models import Quiz


# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'point', 'solved', 'solver',)
