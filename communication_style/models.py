from django.db import models
from django.conf import settings

class CommunicationStyle(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='communicate_like'  # Access with user.skills.all()
    )
    communication_style = models.CharField(max_length=100)

    def __str__(self):
        return self.communication_style
