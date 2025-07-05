from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_applicant, name='landing_applicant'), 
    path('applicant/', views.landing_applicant, name='landing_applicant'), 
    path('employer/', views.landing_employer,name='landing_employer'),

    #display the goat page where we will display application shit
    path('view/job', views.view_job_ad,name='view_job_ad'),
]