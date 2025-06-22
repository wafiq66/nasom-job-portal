from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from document.models import Document
from career_history.models import CareerHistory
from education_vocation_training.models import EducationVocationalTraining
from skill.models import Skill
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# Create your views here.

#PROFILE INFORMATION

#to navigate u to your profile
@login_required
def applicant_profile(request):
    resumes = request.user.uploaded_documents.filter(document_type = 'resume')
    return render(request, 'applicant_profile.html',{'resumes':resumes})

#to update your profile ofcos
@login_required
def update_profile(request):
    if request.method == "POST":
        User = get_user_model()

        user = request.user
              
        #update all the fields
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.city = request.POST.get('city')
        user.state = request.POST.get('state')
        user.phone_number = request.POST.get('phonenumber')
        user.email = request.POST.get('email')
        user.username = request.POST.get('email')
        user.gender = request.POST.get('gender')

        if 'profile_image' in request.FILES:
            if user.profile_image:
                user.profile_image.delete(save=False)  # Delete old image file
            user.profile_image = request.FILES['profile_image']

        if User.objects.exclude(id=user.id).filter(email=user.email).exists():
            messages.error(request, "This email is already in use by another account.")
            return redirect('applicant_profile')

        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('applicant_profile')  # or wherever you want to go
    return render(request, 'applicant_profile.html')

#to upload new resume into the database
@login_required
def upload_resume(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document_file']
        document_type = request.POST.get('document_type')
        base_name = os.path.basename(uploaded_file.name)
        file_name_no_ext = os.path.splitext(base_name)[0]

        document = Document(
            user=request.user,  # assume you're using authentication
            document_file=uploaded_file,
            document_name=file_name_no_ext,
            document_type=document_type,
        )
        document.save()

        messages.success(request, "New Resume Uploaded!")
        return redirect('applicant_profile')  # or wherever you want to go
    return render(request, 'applicant_profile.html') 

#to edit and delete the resume
def manage_resume(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        resume_id = request.POST.get('resume_id')

        resume = get_object_or_404(Document, id=resume_id, user=request.user, document_type='resume')

        if action == 'edit':
            new_name = request.POST.get('document_name', '').strip()
            if new_name:
                resume.document_name = new_name
                resume.save()
                messages.success(request, "Resume Successfully Deleted!")

        elif action == 'delete':
            resume.document_file.delete()
            resume.delete()
            messages.success(request, "Resume Successfully Deleted!")

        return redirect('applicant_profile')
    return render(request, 'applicant_profile.html') 

#BACKGROUND INFORMATION

def applicant_background(request):
    work_histories = request.user.careers.all()
    education_histories = request.user.educations.all()
    skills = request.user.skills.all()
    return render(request,'applicant_background.html',
                  {'work_histories':work_histories,
                   'education_histories':education_histories,
                   'skills':skills})

#for career history
def manage_career_history(request):
    if request.method == "POST":

        job_title_form = request.POST.get('jobtitle')
        company_name_form = request.POST.get('companyname')

        start_date = request.POST.get('startdate')  # "2024-06"
        if start_date:
            year, month = map(int, start_date.split('-'))  # year = 2024, month = 6

        end_date = request.POST.get('enddate')
        if end_date:
            end_year, end_month = map(int, end_date.split('-'))
        else:
            end_year, end_month = None, None

        career = CareerHistory(
            user=request.user,
            job_title=job_title_form,
            company_name=company_name_form,
            start_month = month,
            start_year = year,
            end_month = end_month,
            end_year = end_year
        )

        career.save()

        return redirect('applicant_background')
    return render(request,'applicant_background.html')

#for deleting the career
def delete_career(request, career_id):
    if request.method == 'POST':
        career = get_object_or_404(CareerHistory, id=career_id, user = request.user)
        career.delete()
        return redirect('applicant_background')
    return render(request,'applicant_background.html')

#for updating the career
def update_career(request,career_id):
    if request.method == 'POST':
        career = get_object_or_404(CareerHistory, id=career_id, user = request.user)

        career.job_title = request.POST.get('jobtitle')
        career.company_name = request.POST.get('companyname')

        # Handle startdate
        startdate = request.POST.get('startdate')  # "YYYY-MM"
        if startdate:
            year, month = map(int, startdate.split('-'))
            career.start_year = year
            career.start_month = month

        # Handle enddate
        enddate = request.POST.get('enddate')
        if enddate:
            year, month = map(int, enddate.split('-'))
            career.end_year = year
            career.end_month = month
        else:
            career.end_year = None
            career.end_month = None

        career.save()
        return redirect('applicant_background')
    return render(request,'applicant_background.html')

#for entering education
def manage_education_history(request):
    if request.method == 'POST':
        course_title = request.POST.get('course')
        institution = request.POST.get('institution')

        start_date = request.POST.get('startdate')  # "2024-06"
        if start_date:
            year, month = map(int, start_date.split('-'))  # year = 2024, month = 6

        end_date = request.POST.get('enddate')
        if end_date:
            end_year, end_month = map(int, end_date.split('-'))
        else:
            end_year, end_month = None, None

        edus = EducationVocationalTraining(
            user=request.user,
            course_title=course_title,
            institution=institution,
            start_month = month,
            start_year = year,
            end_month = end_month,
            end_year = end_year
        )

        edus.save()
        return redirect('applicant_background')
    return render(request,'applicant_background.html')

#for deleting the education
def delete_education(request, edu_id):
    if request.method == 'POST':
        edu = get_object_or_404(EducationVocationalTraining, id=edu_id, user = request.user)
        edu.delete()
        return redirect('applicant_background')
    return render(request,'applicant_background.html')

#for updating the education
def update_education(request,edu_id):
    if request.method == 'POST':
        edu = get_object_or_404(EducationVocationalTraining, id=edu_id, user = request.user)

        edu.course_title = request.POST.get('course')
        edu.institution = request.POST.get('institution')

        # Handle startdate
        startdate = request.POST.get('startdate')  # "YYYY-MM"
        if startdate:
            year, month = map(int, startdate.split('-'))
            edu.start_year = year
            edu.start_month = month

        # Handle enddate
        enddate = request.POST.get('enddate')
        if enddate:
            year, month = map(int, enddate.split('-'))
            edu.end_year = year
            edu.end_month = month
        else:
            edu.end_year = None
            edu.end_month = None

        edu.save()
        return redirect('applicant_background')
    return render(request,'applicant_background.html')

#for entering new skill
def manage_skill(request):
    if request.method == 'POST':

        skill_set = request.POST.get('skill')

        skill = Skill(
            user=request.user,
            skill=skill_set
        )

        skill.save()
        return redirect('applicant_background')
    return render(request, 'applicant_background.html')

#for deleting the education
def delete_skill(request, skill_id):
    if request.method == 'POST':
        skill = get_object_or_404(Skill, id=skill_id, user = request.user)
        skill.delete()
        return redirect('applicant_background')
    return render(request,'applicant_background.html')
