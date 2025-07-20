from django.db import models
from django.conf import settings
from document.models import Document
import uuid

# External status choices
VERIFICATION_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("verified", "Verified"),
    ("rejected", "Rejected"),
]

class VerificationRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_verification_request'
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attached_to_verification_request'
    )

    full_name = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)

    organization_name = models.CharField(max_length=255,null=True)
    position = models.CharField(max_length=100,null=True)

    applicant_message = models.TextField(null=True)
    ngo_message = models.TextField(null=True)

    request_date = models.DateField(null=True)
    verified_date = models.DateField(null=True, blank=True)

    verification_status = models.CharField(
        max_length=50,
        choices=VERIFICATION_STATUS_CHOICES,
        default="pending",
        null=True
    )

