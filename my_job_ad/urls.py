from django.urls import path
from . import views

urlpatterns = [
    path('employer/JobAd', views.view_job_table,name='view_job_table'),
    #create/update job ad
    path('employer/JobAd/update/<int:job_id>', views.reload_job,name='reload_job'),
    path('employer/JobAd/post', views.post_job,name='post_job'),
    #close job ad
    path('employer/JobAd/close/<int:job_id>', views.close_job,name='close_job'),
    #delete job ad
    path('employer/JobAd/delete/<int:job_id>', views.delete_job,name='delete_job'),
    #republish job ad
    path('employer/JobAd/republish/<int:job_id>', views.republish_job,name='republish_job'),
]