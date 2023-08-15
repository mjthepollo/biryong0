from django.db import models

from biryong.users.models import User

# Create your models here.

POINT_CHOICES = (
    (30, 30), (40, 40), (50, 50)
)


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    description_image = models.ImageField(
        upload_to="quizs", null=True, blank=True)
    genre = models.CharField(max_length=100)
    point = models.IntegerField(choices=POINT_CHOICES)
    solved = models.BooleanField(default=False)
    answer = models.TextField()
    answer_image = models.ImageField(
        upload_to="quizs", null=True, blank=True)

    solver = models.ForeignKey(
        User, related_name="solved_quizs", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
