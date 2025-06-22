from django.db import models
from django.conf import settings

class PersonalInterest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interest_like'
    )
    personal_interest = models.CharField(max_length=100)

    def __str__(self):
        return self.personal_interest
