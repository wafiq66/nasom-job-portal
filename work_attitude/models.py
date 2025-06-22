from django.db import models
from django.conf import settings

class WorkAttitude(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='work_like'
    )
    work_attitude = models.CharField(max_length=100)

    def __str__(self):
        return self.work_attitude
