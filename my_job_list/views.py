from django.shortcuts import render
from job_application.models import JobApplication

# Create your views here.
def saved_list(request):
    saved_applications = JobApplication.objects.filter(
        user=request.user,
        application_status='saved'
    ).select_related('job_ad')  # <-- job_ad is correct here

    saved_job_ads = [app.job_ad for app in saved_applications]

    return render(request, 'saved_list.html',{
        'saved_job_ads': saved_job_ads
    })

def applied_list(request):
    applied_applications = JobApplication.objects.exclude(
        application_status='saved'
    ).filter(user=request.user).select_related('job_ad')

    return render(request, 'applied_list.html', {
        'applied_job_ads': applied_applications
    })
