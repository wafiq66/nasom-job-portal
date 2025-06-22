from django.db import models
from django.conf import settings

class Skill(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='skills'  # Access with user.skills.all()
    )
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill
