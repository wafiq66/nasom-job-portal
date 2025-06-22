from django.db import models
from django.conf import settings

class CareerHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='careers'  # Access with user.careers.all()
    )
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)

    start_month = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 13)])
    start_year = models.PositiveIntegerField()

    end_month = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 13)],
        null=True, blank=True
    )
    end_year = models.PositiveIntegerField(null=True, blank=True)

    still_in_role = models.BooleanField(default=False)

    def __str__(self):
        if self.still_in_role:
            return f"{self.job_title} at {self.company_name} (Present)"
        return f"{self.job_title} at {self.company_name} ({self.start_month}/{self.start_year} - {self.end_month}/{self.end_year})"
