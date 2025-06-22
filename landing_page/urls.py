from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_applicant, name='landing_applicant'), 
    path('applicant/', views.landing_applicant, name='landing_applicant'), 
    path('employer/', views.landing_employer,name='landing_employer'),
]