from django.urls import path
from . import views

urlpatterns = [
    path('employer/JobAd', views.view_job_table,name='view_job_table')
]