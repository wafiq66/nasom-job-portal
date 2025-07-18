from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from job_ad.models import JobAd
from document.models import Document
from job_application.models import JobApplication
from django.utils import timezone

# Create your views here.

User = get_user_model()

def landing_applicant(request):
    jobs = JobAd.objects.filter(publish_status='active')
    return render(request,"landing_applicant.html",{'jobs':jobs})

def landing_employer(request):
    return render(request,"landing_employer.html")

#this one is used to render the specific job ad that clicked by the user
def view_job_ad(request,job_id):
    resume_docs = Document.objects.filter(user=request.user, document_type='resume')
    job_ad = get_object_or_404(JobAd,id=job_id,user=request.user)
    saved = False
    existing_application = JobApplication.objects.filter(user=request.user, job_ad=job_ad).first()

    if existing_application and existing_application.application_status:
        saved = existing_application.application_status.lower() == "saved"

    return render(request,'job_apply.html',{
        'job_ad':job_ad,
        'user_resumes':resume_docs,
        'saved':saved,
        })

#this one to register the application of the user into the database
def register_application(request):
    if request.method == 'POST':
        #to read the input from the user
        job_id = request.POST.get("jobid")
        answer1 = request.POST.get("answer1")
        answer2 = request.POST.get("answer2")
        answer3 = request.POST.get("answer3")
        resume_id = request.POST.get("resume")

        job_ad = get_object_or_404(JobAd, id=job_id)
        document = None
        if resume_id:
            document = get_object_or_404(Document, id=resume_id)
        
        #to check whether the application or exist or not
        existing_application = JobApplication.objects.filter(user=request.user, job_ad=job_ad).first()
        #if the application exist then it go here
        if existing_application:
            status = existing_application.application_status.lower()
             # Allow re-application if status is 'rejected' or 'saved'
            if status in [None,'rejected', 'saved','called']:
                existing_application.answer_one = answer1
                existing_application.answer_two = answer2
                existing_application.answer_three = answer3
                existing_application.document = document
                existing_application.application_status = 'pending'
                existing_application.date_applied = timezone.now()
                existing_application.save()

                messages.success(request, "Your application has been submitted.")
                return redirect("view_job_ad", job_id=job_ad.id)
            else:
                messages.warning(request, "You have already applied for this job.")
                return redirect("view_job_ad", job_id=job_ad.id)
            
        #if not exist then it go here
        else :    
            #submit application if there is no application been made
            JobApplication.objects.create(
                user=request.user,
                job_ad=job_ad,
                answer_one=answer1,
                answer_two=answer2,
                answer_three=answer3,
                document=document,
                date_applied = timezone.now(),
                application_status="pending",
            )

            messages.success(request, "Your application has been submitted.")
            return redirect("view_job_ad", job_id=job_ad.id)

    return render(request,"job_apply.html")

def toggle_save(request):
    if request.method == "POST":
        job_id = request.POST.get("jobid")
        job_ad = get_object_or_404(JobAd, id=job_id)

        existing_application = JobApplication.objects.filter(user=request.user, job_ad=job_ad).first()

        if existing_application:
            status = existing_application.application_status.lower() if existing_application.application_status else None

            # Allow toggle only if current status is None or rejected
            if status in [None, "rejected","saved"]:
                if status == "saved":
                    # Unsave
                    existing_application.application_status = None
                    messages.success(request, "Job has been unsaved.")
                else:
                    # Save
                    existing_application.application_status = "saved"
                    messages.success(request, "Job has been saved.")
                
                existing_application.save()
                return redirect("view_job_ad", job_id=job_ad.id)

            else:
                messages.warning(request, "You have already applied for this job and cannot save it.")
                return redirect("view_job_ad", job_id=job_ad.id)

        else:
            # No existing application: allow save
            JobApplication.objects.create(
                user=request.user,
                job_ad=job_ad,
                application_status="saved",
            )
            messages.success(request, "Job has been saved.")
            return redirect("view_job_ad", job_id=job_ad.id)

    return render(request,"job_apply.html")  # or your default fallback page

def view_applicant_recruit(request):
    return render(request,'applicant_recruit.html')

def hiring_advice(request):
    return render(request,'hiring_advice.html')

def search_company(request):
    users = User.objects.filter(company_name__isnull=False).exclude(company_name='')
    return render(request,'search_company.html',{
        'companies':users,
    })

def view_company(request,company_id):
    company = User.objects.filter(id=company_id).first()
    jobs = company.post_job.filter(publish_status='active')
    return render(request,'view_company.html',{
        'company':company,
        'jobs':jobs,
    })