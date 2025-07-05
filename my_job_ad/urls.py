from django.urls import path
from . import views

urlpatterns = [
    path('employer/JobAd', views.view_job_table,name='view_job_table'),
    #create/update job ad
    path('employer/JobAd/form', views.reload_job,name='reload_job'),
    path('employer/JobAd/save', views.post_job,name='post_job'),
]