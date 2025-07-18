from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_applicant, name='landing_applicant'), 
    path('applicant/', views.landing_applicant, name='landing_applicant'), 
    path('employer/', views.landing_employer,name='landing_employer'),

    #display the goat page where we will display application shit
    path('view/job/<int:job_id>', views.view_job_ad,name='view_job_ad'),
    path('view/applicant', views.view_applicant_recruit,name='view_applicant_recruit'),

    #display the hiring advice page
    path('hiring/advice', views.hiring_advice, name='hiring_advice'),

    #display the search company page
    path('search/company', views.search_company, name='search_company'),

    #display the view company page
    path('view/company/<int:company_id>', views.view_company, name='view_company'),

    #this one is to submit application into the database
    path('view/job/submit/application', views.register_application, name='register_application'),
    #this one is used to toggle job save into the database
    path('view/job/save', views.toggle_save, name='toggle_save'),
]