from django import forms

from biryong.quiz.models import Quiz


class SolveForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('solver',)
