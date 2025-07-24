from django.shortcuts import render
from django.shortcuts import redirect
from job_ad.models import JobAd
from job_application.models import JobApplication
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def applicant_list(request):
     # Step 1: Get job ads posted by the current user (the company)
    job_ads = JobAd.objects.filter(user=request.user)

    # Step 2: Get applications to those job ads, excluding "Saved"
    applicants = JobApplication.objects.filter(
        job_ad__in=job_ads
    ).exclude(application_status__in=['saved', None])

    return render(request, 'applicant_list.html',{
        'applicants': applicants,
        'job_ads':job_ads,
    })

@login_required
def shortlist_applicant(request,application_id):

    application = get_object_or_404(JobApplication, id=application_id)
    application.application_status = 'shortlisted'
    application.save()

    return redirect("applicant_list")

@login_required
def accept_applicant(request,application_id):

    application = get_object_or_404(JobApplication, id=application_id)
    application.application_status = 'accepted'
    application.save()

    return redirect("applicant_list")

@login_required
def reject_applicant(request,application_id):

    application = get_object_or_404(JobApplication, id=application_id)
    application.application_status = 'rejected'
    application.save()

    return redirect("applicant_list")

@login_required
def applicant_manage(request,application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    if request.method == 'POST':
        read_application_status = request.POST.get('application_status')
        application.application_status = read_application_status
        application.save()
        
        return redirect('applicant_manage',application_id)
    return render(request, 'applicant_manage.html',{
        'application':application,
    })
