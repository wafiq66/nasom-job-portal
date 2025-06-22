from django.urls import path
from . import views

urlpatterns = [
    #Section page for basic information
    path('applicant/profile', views.applicant_profile, name='applicant_profile'),  
    path('applicant/profile/update',views.update_profile, name='update_profile'),
    path('applicant/profile/resume/upload',views.upload_resume,name='upload_resume'),
    path('applicant/profile/resume/update', views.manage_resume,name='manage_resume'),
    #Section page for career history, education history, skills
    path('applicant/profile/background', views.applicant_background,name='applicant_background'),
]
