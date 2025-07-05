from django.urls import path
from . import views

urlpatterns = [
    path('applicant/saved',views.saved_list,name='saved_list'),
    path('applicant/applied',views.applied_list,name='applied_list'),
]