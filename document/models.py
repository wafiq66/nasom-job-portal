from django.db import models
import os
from application_user.models import ApplicationUser

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('resume', 'Resume'),
        ('verification', 'Verification'),
    ]

    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE, related_name='uploaded_documents')
    document_file = models.FileField(upload_to='documents/')
    document_name = models.CharField(max_length=255, blank=True)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    uploaded_date = models.DateTimeField(auto_now_add=True)

