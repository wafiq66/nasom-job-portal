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

    start_month = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 13)])
    start_year = models.PositiveIntegerField()
    end_month = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 13)], null=True, blank=True)
    end_year = models.PositiveIntegerField(null=True, blank=True)

    @property
    def display_range(self):
        start_str = f"{calendar.month_name[self.start_month]} {self.start_year}"
        if self.end_month and self.end_year:
            end_str = f"{calendar.month_name[self.end_month]} {self.end_year}"
        else:
            end_str = "Present"
        return f"{start_str} - {end_str}"

    @property
    def start_month_input(self):
        return f"{self.start_year}-{self.start_month:02d}"

    @property
    def end_month_input(self):
        if self.end_year and self.end_month:
            return f"{self.end_year}-{self.end_month:02d}"
        return ""

    def __str__(self):
        status = "Completed" if self.completion_status else "In Progress"
        return f"{self.course_title} at {self.institution} ({status})"
