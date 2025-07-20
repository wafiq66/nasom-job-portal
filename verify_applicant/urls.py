from django.urls import path
from . import views

urlpatterns = [
    path('ngo/verify/applicant/<uuid:vr_id>', views.verify_applicant, name='verify_applicant'),
]
