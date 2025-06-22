from django.db import models
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

    completion_status = models.BooleanField(default=False)  # True = Completed, False = In Progress

    def __str__(self):
        status = "Completed" if self.completion_status else "In Progress"
        return f"{self.course_title} at {self.institution} ({status})"
