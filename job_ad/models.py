from django.db import models
from django.conf import settings

class JobAd(models.Model):

    PUBLISH_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]

    JOB_CATEGORY_CHOICES = [
        ('professional', 'Professional Job'),
        ('semi', 'Semi-Skilled Job'),
        ('simple', 'Simple Job'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_job'
    )

    #Job Classification
    job_title = models.CharField(max_length=255)

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
    calming_space_status = models.BooleanField(default=False)
    calming_space_desc = models.TextField(blank=True, null=True)

    full_flexible_status = models.BooleanField(default=False)
    shift_pool_status = models.BooleanField(default=False)
    shift_flexicle_desc = models.TextField(blank=True, null=True)

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
