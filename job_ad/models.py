from django.db import models
from django.conf import settings
from rapidfuzz import fuzz

class JobAd(models.Model):

    PUBLISH_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]

    JOB_CATEGORY_CHOICES = [
        ('Professional Job', 'Professional Job'),
        ('Semi-Skilled Job', 'Semi-Skilled Job'),
        ('Simple Job', 'Simple Job'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_job'
    )

    #Job Classification
    job_title = models.CharField(blank=True,max_length=255)
    job_location = models.CharField(blank=True,max_length=255)
    for_level_one = models.BooleanField(default=False)
    for_level_two = models.BooleanField(default=False)
    for_level_three = models.BooleanField(default=False)

    job_category = models.CharField(
        max_length=20,
        choices=JOB_CATEGORY_CHOICES,
        blank=True,
        null=True
    )

    can_full_time = models.BooleanField(default=False)
    can_part_time = models.BooleanField(default=False)
    can_remote = models.BooleanField(default=False)

    minimum_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    maximum_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    #Detailed Job Textual Description
    main_task_desc = models.TextField(blank=True, null=True)
    sub_task_status = models.BooleanField(default=False)
    sub_task_desc = models.TextField(blank=True, null=True)

    repetitive_task_status = models.BooleanField(default=False)
    easy_to_perform_status = models.BooleanField(default=False)
    easy_to_remember_status = models.BooleanField(default=False)

    interaction_with_cust_status = models.BooleanField(default=False)
    interaction_with_cust_desc = models.TextField(blank=True, null=True)

    verbal_interview_status = models.BooleanField(default=False)
    verbal_interview_desc = models.TextField(blank=True, null=True)

    nonverbal_interview_status = models.BooleanField(default=False)
    nonverbal_interview_desc = models.TextField(blank=True, null=True)

    representative_interview_status = models.BooleanField(default=False)
    representative_interview_desc = models.TextField(blank=True, null=True)

    no_interview_status = models.BooleanField(default=False)

    special_training_status = models.BooleanField(default=False)
    special_training_desc = models.TextField(blank=True, null=True)

    one_training_status = models.BooleanField(default=False)
    multiple_training_status = models.BooleanField(default=False)
    time_training_desc = models.TextField(blank=True, null=True)

    work_buddy_status = models.BooleanField(default=False)
    work_buddy_desc = models.TextField(blank=True, null=True)

    mentor_status = models.BooleanField(default=False)
    mentor_desc = models.TextField(blank=True, null=True)

    less_noisy_env_status = models.BooleanField(default=False)
    less_stressful_env_status = models.BooleanField(default=False)
    calming_space_status = models.BooleanField(default=False)
    calming_space_desc = models.TextField(blank=True, null=True)

    full_flexible_status = models.BooleanField(default=False)
    shift_pool_status = models.BooleanField(default=False)
    shift_flexible_desc = models.TextField(blank=True, null=True)

    regular_update_status = models.BooleanField(default=False)
    regular_update_desc = models.TextField(blank=True, null=True)

    full_transport_status = models.BooleanField(default=False)
    partial_transport_status = models.BooleanField(default=False)
    transport_desc = models.TextField(blank=True, null=True)

    other_status = models.BooleanField(default=False)
    other_desc = models.TextField(blank=True, null=True)
    
    #Question section
    question_one = models.TextField(blank=True, null=True)
    question_two = models.TextField(blank=True, null=True)
    question_three = models.TextField(blank=True, null=True)

    publish_status = models.CharField(
        max_length=10,
        choices=PUBLISH_STATUS_CHOICES,
        default='draft'
    )
    publish_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.job_title
    
    def get_city(self):
        """Extract city from job_location"""
        if self.job_location:
            location_parts = self.job_location.split(',')
            if len(location_parts) >= 1:
                return location_parts[0].strip()
        return ""
    
    def get_state(self):
        """Extract state from job_location"""
        if self.job_location:
            location_parts = self.job_location.split(',')
            if len(location_parts) >= 2:
                return location_parts[1].strip()
        return ""

    def format_question(self, question):
        if not question:
            return ''
        question = question.strip()
        # Remove all trailing ? and add one
        question = question.rstrip('?') + '?'
        return question
    
    def get_question_one(self):
        return self.format_question(self.question_one)

    def get_question_two(self):
        return self.format_question(self.question_two)

    def get_question_three(self):
        return self.format_question(self.question_three)
    
    def has_any_benefit_status(self):
        return any([
            self.special_training_status,
            self.one_training_status,
            self.multiple_training_status,
            self.work_buddy_status,
            self.mentor_status,
            self.less_noisy_env_status,
            self.less_stressful_env_status,
            self.calming_space_status,
            self.full_flexible_status,
            self.shift_pool_status,
            self.regular_update_status,
            self.full_transport_status,
            self.partial_transport_status
        ])
    
    def has_any_interview_option(self):
        return any([
            self.verbal_interview_status,
            self.nonverbal_interview_status,
            self.representative_interview_status,
            self.no_interview_status
        ])
    
    def calculate_relevance_score(self):
        score = 0

        # Basic info
        if self.job_title:
            score += 2
        if self.job_location:
            score += 2

        # Job classification
        if self.for_level_one or self.for_level_two or self.for_level_three:
            score += 5

        # Salary range
        if self.minimum_salary and self.maximum_salary:
            score += 3

        # Job category
        if self.job_category:
            score += 1

        # Employment type
        for field in ['can_full_time', 'can_part_time', 'can_remote']:
            if getattr(self, field):
                score += 1

        # Description fields
        desc_fields = [
            'main_task_desc', 'sub_task_desc', 'interaction_with_cust_desc',
            'verbal_interview_desc', 'nonverbal_interview_desc', 'representative_interview_desc',
            'special_training_desc', 'time_training_desc', 'work_buddy_desc', 'mentor_desc',
            'calming_space_desc', 'shift_flexible_desc', 'regular_update_desc', 'transport_desc', 'other_desc'
        ]
        
        for field in desc_fields:
            if getattr(self, field):
                score += 2

        # Boolean support flags
        boolean_fields = [
            'sub_task_status', 'repetitive_task_status', 'easy_to_perform_status',
            'easy_to_remember_status', 'interaction_with_cust_status',
            'verbal_interview_status', 'nonverbal_interview_status',
            'representative_interview_status', 'no_interview_status',
            'special_training_status', 'one_training_status', 'multiple_training_status',
            'work_buddy_status', 'mentor_status', 'less_noisy_env_status',
            'less_stressful_env_status', 'calming_space_status',
            'full_flexible_status', 'shift_pool_status', 'regular_update_status',
            'full_transport_status', 'partial_transport_status', 'other_status'
        ]

        for field in boolean_fields:
            if getattr(self, field):
                score += 1

        # Optional: question fields
        if self.question_one and self.question_two and self.question_three:
            score += 10

        return score

    def apply_filter_score(self,minpaysalary,job_professional,job_semiskilled,job_simple,work_full,work_part,work_remote,for_aut_1,for_aut_2,for_aut_3):
        score = 0

        if self.minimum_salary is not None and self.minimum_salary >= minpaysalary:
            score += 50
        #filter out by the category
        if job_professional and self.job_category == 'Professional Job':
            score+=50
        if job_semiskilled and self.job_category == 'Semi-Skilled Job':
            score+=50
        if job_simple and self.job_category == 'Simple Job':
            score+=50
        #filter out by can full time, part time, remote
        if work_full and self.can_full_time:
            score+=50
        if work_part and self.can_part_time:
            score+=50
        if work_remote and self.can_remote:
            score+=50
        #filter out by autism level
        if for_aut_1 and self.for_level_one:
            score+=50
        if for_aut_2 and self.for_level_two:
            score+=50
        if for_aut_3 and self.for_level_three:
            score+=50
        print(f"{self.job_title}: {score}")
        return score

    def keyword_location_score(self,keyword,locations):
        score = 0

        if keyword:
            #calculate the keyword jobtitle or company name similarities
            similarity = fuzz.ratio(self.job_title.lower(), keyword.lower())
            if similarity > 70:
                score += (similarity*2)  # or some weighted score
            elif similarity > 50:
                score += (similarity)  # or some weighted score
            similarity = fuzz.ratio(self.user.company_name.lower() , keyword.lower())
            if similarity > 70:
                score += (similarity)  # or some weighted score
            elif similarity > 50:
                score += (similarity/2)  # or some weighted score
        if locations:
            #calculate the location similarities. for city and state
            for location in locations:
                similarity = fuzz.ratio(self.get_city().lower(), location.lower())
                if similarity > 90:
                    score += (similarity*2)  # or some weighted score
                elif similarity > 80:
                    score += (similarity)  # or some weighted score
                similarity = fuzz.ratio(self.get_state().lower(), location.lower())
                if similarity > 90:
                    score += (similarity*2)  # or some weighted score
                elif similarity > 80:
                    score += (similarity)  # or some weighted score

        print(f"{self.job_title}: {score}")
        return score