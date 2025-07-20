from django.contrib.auth.models import AbstractUser
from django.db import models

class ApplicationUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    You can add your custom fields below.
    """
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    # 🔽 Add your custom fields here
    # Personal Information
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )


    # Contact/Address Applicant
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    #biography
    biography = models.TextField(blank=True, null=True)

    # Company-related (for employer accounts)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    company_logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True
    )

    #to ensure the user is not dependent
    looking_job_status = models.BooleanField(default=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_location(self):
        return f"{self.city}, {self.state}".strip(', ')

    def get_latest_verification_request(self):
        return self.sent_verification_request.order_by('-request_date').first()

    def check_verification_status(self):
        vr = self.get_latest_verification_request()
        if vr:
            if vr.verification_status == 'verified':
                return True
            else:
                return False
        else:
            return False
        
    def get_verifier_name(self):
        vr = self.get_latest_verification_request()
        if vr:
            return vr.full_name
        else:
            return None
        
    def get_verifier_organization(self):
        vr = self.get_latest_verification_request()
        if vr:
            return vr.organization_name
        else:
            return None
        
    def get_verifier_position(self):
        vr = self.get_latest_verification_request()
        if vr:
            return vr.position
        else:
            return None
        
    def get_verifier_message(self):
        vr = self.get_latest_verification_request()
        if vr:
            return vr.ngo_message
        else:
            return None

    # 🔽 Optional: toString representation
    def __str__(self):
        return self.username