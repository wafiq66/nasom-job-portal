from django.urls import path
from . import views

urlpatterns = [
    path('ngo/verify/applicant', views.verify_applicant, name='verify_applicant'),
]
