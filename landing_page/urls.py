from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_applicant, name='landing_applicant'), 
    path('applicant/', views.landing_applicant, name='landing_applicant'), 
    path('employer/', views.landing_employer,name='landing_employer'),

    #display the goat page where we will display application shit
    path('view/job', views.view_job_ad,name='view_job_ad'),
    path('view/applicant', views.view_applicant_recruit,name='view_applicant_recruit'),

    #display the hiring advice page
    path('hiring/advice', views.hiring_advice, name='hiring_advice'),

    #display the search company page
    path('search/company', views.search_company, name='search_company'),

    #display the view company page
    path('view/company', views.view_company, name='view_company'),
]