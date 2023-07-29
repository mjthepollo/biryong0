from django.db import models

from config.models import TimeStampedModel

# Create your models here.


class SmallTalk(TimeStampedModel):
    class Meta:
        ordering = ['created']
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    message = models.TextField()
