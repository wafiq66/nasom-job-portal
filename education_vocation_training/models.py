from django.db import models
import calendar
from django.conf import settings

class EducationVocationalTraining(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='educations'  # user.educations.all()
    )
    course_title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)

    end_month = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 13)], null=True, blank=True)
    end_year = models.PositiveIntegerField(null=True, blank=True)

    @property
    def end_month_input(self):
        if self.end_year and self.end_month:
            return f"{self.end_year}-{self.end_month:02d}"
        return ""

    def __str__(self):
        status = "Completed" if self.completion_status else "In Progress"
        return f"{self.course_title} at {self.institution} ({status})"
