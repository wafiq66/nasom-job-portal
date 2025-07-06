from django.urls import path
from . import views

urlpatterns = [
    path('employer/applicant-list/', views.applicant_list, name='applicant_list'),
    path('employer/applicant-manage/', views.applicant_manage, name='applicant_manage'),
]