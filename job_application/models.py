from django.db import models
from django.conf import settings  # for referencing the User model
from job_ad.models import JobAd  
from document.models import Document
from django.utils import timezone

class JobApplication(models.Model):

    STATUS_CHOICES = [
        ('saved', 'Saved'),
        ('called', 'Called by Employer'),
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='make_applications')
    job_ad = models.ForeignKey(
        JobAd, 
        on_delete=models.CASCADE, 
        related_name='has_applications')
    document = models.ForeignKey(
        Document, on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='used_in_applications')
    
    application_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending',null=True)

    date_applied = models.DateTimeField(null=True, blank=True)
    answer_one = models.TextField(blank=True, null=True)
    answer_two = models.TextField(blank=True, null=True)
    answer_three = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'job_ad')  # ⬅ Prevent same user from applying to the same job twice


    def applied_current_date(self):
        self.date_applied = timezone.now()

    def display_applied_date(self):
        now = timezone.now()
        delta = now - self.date_applied

        if delta.days < 1:
            return "Today"
        elif delta.days == 1:
            return "1 day ago"
        elif delta.days < 7:
            return f"{delta.days} days ago"
        else:
            return self.date_applied.strftime("%d %B %Y")  # e.g., 16 July 2025

    def display_applied_date_iso(self):
        return self.date_applied.strftime("%Y-%m-%d")


    def __str__(self):
        return f"{self.user.username} applied to {self.job_ad.title}"
