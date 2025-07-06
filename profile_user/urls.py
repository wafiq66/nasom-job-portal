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

    path('applicant/profile/background/career', views.manage_career_history,name='applicant_background_career'),
    path('applicant/profile/background/career/delete/<int:career_id>', views.delete_career,name='delete_career'),
    path('applicant/profile/background/career/update/<int:career_id>', views.update_career,name='update_career'),

    path('applicant/profile/background/education', views.manage_education_history,name='applicant_education'),
    path('applicant/profile/background/education/delete/<int:edu_id>', views.delete_education,name='delete_education'),
    path('applicant/profile/background/education/update/<int:edu_id>', views.update_education,name='update_education'),
    #Section for skill
    path('applicant/profile/background/skill', views.manage_skill,name='applicant_skill'),
    path('applicant/profile/background/skill/delete/<int:skill_id>', views.delete_skill,name='delete_skill'),


    #Section page for Autistic Profile
    path('applicant/profile/autistic', views.applicant_autistic_profile, name='applicant_autistic_profile'),
    path('applicant/profile/autistic/workattitude', views.manage_work_attitude, name='applicant_work_attitude'),
    path('applicant/profile/autistic/workattitude/delete/<int:attitude_id>', views.delete_work_attitude,name='delete_work_attitude'),
    path('applicant/profile/autistic/communicationstyle', views.manage_communication_style, name='applicant_communication_style'),
    path('applicant/profile/autistic/communicationstyle/delete/<int:com_id>', views.delete_communication_style,name='delete_communication_style'),
    path('applicant/profile/autistic/personalinterest', views.manage_personal_interest, name='applicant_personal_interest'),
    path('applicant/profile/autistic/personalinterest/delete/<int:interest_id>', views.delete_personal_interest,name='delete_personal_interest'),


    #Section page to view employer profile

    path('employer/profile', views.employer_profile,name='employer_profile'),
    path('employer/profile/update', views.update_employer_profile,name='update_employer_profile'),

    #Section page to view applicant verification request
    path('applicant/profile/verification/request', views.applicant_verification_request,name='applicant_verification_request'),

    #Section page to view change password form
    path('applicant/profile/change/password', views.change_password, name='change_password'),
]
