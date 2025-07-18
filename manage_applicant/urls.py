from django.urls import path
from . import views

urlpatterns = [
    path('employer/applicant-list/', views.applicant_list, name='applicant_list'),
    path('employer/applicant-manage/<int:application_id>', views.applicant_manage, name='applicant_manage'),

    #to change the status at applicant list
    path('employer/application/shortlist/<int:application_id>', views.shortlist_applicant, name='shortlist_applicant'),
    path('employer/application/accept/<int:application_id>', views.accept_applicant, name='accept_applicant'),
    path('employer/application/reject/<int:application_id>', views.reject_applicant, name='reject_applicant'),
]