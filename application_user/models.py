from django.contrib.auth.models import AbstractUser
from django.db import models
from rapidfuzz import fuzz

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

    def get_company_city(self):
        if self.company_address:
            parts = [p.strip() for p in self.company_address.split(',')]
            if len(parts) >= 1:
                return parts[0]
        return None

    def get_company_state(self):
        if self.company_address:
            parts = [p.strip() for p in self.company_address.split(',')]
            if len(parts) >= 2:
                return parts[1]
        return None


    #calculate relevance score of the company
    def get_company_relevance_score(self):
        score = 0

        if self.company_name:
            score += 30
        if self.company_address:
            score += 20
        if self.company_description:
            score += 30
        if self.company_logo:
            score += 20

        print(f"{self.company_name}:Relevance : {score}")
        return score
    #relevance score of the company
    def keyword_location_score(self,keyword,locations):
        score = 0

        if keyword:
            similarity = fuzz.ratio(self.company_name.lower() , keyword.lower())
            if similarity > 70:
                score += (similarity)  # or some weighted score
            elif similarity > 50:
                score += (similarity/2)  # or some weighted score
        if locations:
            #calculate the location similarities. for city and state
            for location in locations:
                similarity = fuzz.ratio(self.get_company_city().lower(), location.lower())
                if similarity > 90:
                    score += (similarity*2)  # or some weighted score
                elif similarity > 80:
                    score += (similarity)  # or some weighted score
                similarity = fuzz.ratio(self.get_company_state().lower(), location.lower())
                if similarity > 90:
                    score += (similarity*2)  # or some weighted score
                elif similarity > 80:
                    score += (similarity)  # or some weighted score
        print(f"{self.company_name}: Search : {score}")
        return score
    
    #calculate relevance score of the user
    def get_applicant_relevance_score(self):
        score = 0

        if self.first_name:
            score += 30
        if self.last_name:
            score += 30
        if self.gender:
            score += 30
        if self.phone_number:
            score += 30
        if self.email:
            score += 30
        if self.city:
            score += 30
        if self.state:
            score += 30
        if self.biography:
            score += 30

        if self.uploaded_documents.filter(document_type='resume'):
            score +=10
        if self.careers.all():
            score +=20
        if self.educations.all():
            score +=20
        if self.skills.all():
            score +=20
        if self.interest_like.all():
            score +=20
        if self.work_like.all():
            score +=20
        if self.communicate_like.all():
            score +=20

        if self.sent_verification_request.filter(verification_status = 'verified'):
            score += 700

        print(f"{self.get_full_name()}: Relevant : {score}")
        return score

    def applicant_keyword_location_score(self,keyword,locations):
        score = 0

        if keyword:
            #this one check first name
            similarity = fuzz.ratio(self.first_name.lower() , keyword.lower())
            if similarity > 70:
                score += (similarity)  # or some weighted score
            elif similarity > 50:
                score += (similarity/2)  # or some weighted score
            #this one check last name
            similarity = fuzz.ratio(self.last_name.lower() , keyword.lower())
            if similarity > 70:
                score += (similarity)  # or some weighted score
            elif similarity > 50:
                score += (similarity/2)  # or some weighted score

            for job_history in self.careers.all():
                similarity = fuzz.ratio(job_history.job_title.lower() , keyword.lower())
                if similarity > 80:
                    score += (similarity)  # or some weighted score
                elif similarity > 50:
                    score += (similarity/2)  # or some weighted score
            
            for edu_history in self.educations.all():
                similarity = fuzz.ratio(edu_history.course_title.lower() , keyword.lower())
                if similarity > 80:
                    score += (similarity)  # or some weighted score
                elif similarity > 50:
                    score += (similarity/2)  # or some weighted score
            
            for skill in self.skills.all():
                similarity = fuzz.ratio(skill.skill.lower() , keyword.lower())
                if similarity > 80:
                    score += (similarity)  # or some weighted score
                elif similarity > 50:
                    score += (similarity/2)  # or some weighted score
                
            for interest in self.interest_like.all():
                similarity = fuzz.ratio(interest.personal_interest.lower() , keyword.lower())
                if similarity > 80:
                    score += (similarity)  # or some weighted score
                elif similarity > 50:
                    score += (similarity/2)  # or some weighted score

            for work_like in self.work_like.all():
                similarity = fuzz.ratio(work_like.work_attitude.lower() , keyword.lower())
                if similarity > 80:
                    score += (similarity)  # or some weighted score
                elif similarity > 50:
                    score += (similarity/2)  # or some weighted score

            for com_like in self.communicate_like.all():
                similarity = fuzz.ratio(com_like.communication_style.lower() , keyword.lower())
                if similarity > 80:
                    score += (similarity)  # or some weighted score
                elif similarity > 50:
                    score += (similarity/2)  # or some weighted score

        if locations:
            #calculate the location similarities. for city and state
            for location in locations:
                similarity = fuzz.ratio(self.city.lower(), location.lower())
                if similarity > 90:
                    score += (similarity*2)  # or some weighted score
                elif similarity > 80:
                    score += (similarity)  # or some weighted score
                similarity = fuzz.ratio(self.state.lower(), location.lower())
                if similarity > 90:
                    score += (similarity*2)  # or some weighted score
                elif similarity > 80:
                    score += (similarity)  # or some weighted score
        print(f"{self.company_name}: Search : {score}")
        return score
  
    # 🔽 Optional: toString representation
    def __str__(self):
        return self.username