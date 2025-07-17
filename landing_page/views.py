from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from job_ad.models import JobAd
from document.models import Document

# Create your views here.

def landing_applicant(request):
    jobs = JobAd.objects.all()
    return render(request,"landing_applicant.html",{'jobs':jobs})

def landing_employer(request):
    return render(request,"landing_employer.html")

#this one is used to render the specific job ad that clicked by the user
def view_job_ad(request,job_id):
    resume_docs = Document.objects.filter(user=request.user, document_type='resume')
    job_ad = get_object_or_404(JobAd,id=job_id,user=request.user)
    return render(request,'job_apply.html',{
        'job_ad':job_ad,
        'user_resumes':resume_docs,
        })

def view_applicant_recruit(request):
    return render(request,'applicant_recruit.html')

def hiring_advice(request):
    return render(request,'hiring_advice.html')

def search_company(request):
    return render(request,'search_company.html')

def view_company(request):
    return render(request,'view_company.html')