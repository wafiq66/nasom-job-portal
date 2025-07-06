from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from document.models import Document
from career_history.models import CareerHistory
from education_vocation_training.models import EducationVocationalTraining

from work_attitude.models import WorkAttitude
from communication_style.models import CommunicationStyle
from personal_interest.models import PersonalInterest

from skill.models import Skill
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
import pandas as pd
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
        user.biography = request.POST.get('biography')
        
        if User.objects.exclude(id=user.id).filter(email=user.email).exists():
            messages.error(request, "This email is already in use by another account.")
            return redirect('applicant_profile')

        if 'profile_image' in request.FILES:
            if user.profile_image:
                user.profile_image.delete(save=False)  # Delete old image file
            user.profile_image = request.FILES['profile_image']

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
@login_required
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
@login_required
def applicant_background(request):
    work_histories = request.user.careers.all()
    education_histories = request.user.educations.all()
    skills = request.user.skills.all()
    return render(request,'applicant_background.html',
                  {'work_histories':work_histories,
                   'education_histories':education_histories,
                   'skills':skills})

#for career history
@login_required
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
@login_required
def delete_career(request, career_id):
    if request.method == 'POST':
        career = get_object_or_404(CareerHistory, id=career_id, user = request.user)
        career.delete()
        return redirect('applicant_background')
    return render(request,'applicant_background.html')

#for updating the career
@login_required
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
@login_required
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
@login_required
def delete_education(request, edu_id):
    if request.method == 'POST':
        edu = get_object_or_404(EducationVocationalTraining, id=edu_id, user = request.user)
        edu.delete()
        return redirect('applicant_background')
    return render(request,'applicant_background.html')

#for updating the education
@login_required
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
@login_required
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
@login_required
def delete_skill(request, skill_id):
    if request.method == 'POST':
        skill = get_object_or_404(Skill, id=skill_id, user = request.user)
        skill.delete()
        return redirect('applicant_background')
    return render(request,'applicant_background.html')


#for navigation to autistic profile page
@login_required
def applicant_autistic_profile(request):
    work_attitude = request.user.work_like.all()
    communication_style = request.user.communicate_like.all()
    personal_interest = request.user.interest_like.all()
    return render(request, 'applicant_autistic_profile.html',
                  {
                      'work_attitudes':work_attitude,
                      'communication_styles':communication_style,
                      'personal_interests':personal_interest
                  })

#for entering new work attitude
@login_required
def manage_work_attitude(request):
    if request.method == 'POST':

        work_set = request.POST.get('workattitude')

        work_attitude = WorkAttitude(
            user=request.user,
            work_attitude=work_set
        )

        work_attitude.save()
        return redirect('applicant_autistic_profile')
    return render(request, 'applicant_autistic_profile.html')

#delete work attitude
@login_required
def delete_work_attitude(request, attitude_id):
    if request.method == 'POST':
        work_attitude = get_object_or_404(WorkAttitude, id=attitude_id, user = request.user)
        work_attitude.delete()
        return redirect('applicant_autistic_profile')
    return render(request,'applicant_autistic_profile.html')

#for entering new communication style
@login_required
def manage_communication_style(request):
    if request.method == 'POST':

        communication_set = request.POST.get('communicationstyle')

        communication_style = CommunicationStyle(
            user=request.user,
            communication_style=communication_set
        )

        communication_style.save()
        return redirect('applicant_autistic_profile')
    return render(request, 'applicant_autistic_profile.html')

#delete communication style
@login_required
def delete_communication_style(request, com_id):
    if request.method == 'POST':
        communication_style = get_object_or_404(CommunicationStyle, id=com_id, user = request.user)
        communication_style.delete()
        return redirect('applicant_autistic_profile')
    return render(request,'applicant_autistic_profile.html')

#for entering new personal interest
@login_required
def manage_personal_interest(request):
    if request.method == 'POST':

        interest_set = request.POST.get('personalinterest')

        personal_interest = PersonalInterest(
            user=request.user,
            personal_interest=interest_set
        )

        personal_interest.save()
        return redirect('applicant_autistic_profile')
    return render(request, 'applicant_autistic_profile.html')

#delete personal interest
@login_required
def delete_personal_interest(request, interest_id):
    if request.method == 'POST':
        personal_interest = get_object_or_404(PersonalInterest, id=interest_id, user = request.user)
        personal_interest.delete()
        return redirect('applicant_autistic_profile')
    return render(request,'applicant_autistic_profile.html')

#view employer profile
@login_required
def employer_profile(request):
    return render(request, 'employer_profile.html')

#update employer profile LETSS GOO
@login_required
def update_employer_profile(request):
    if request.method == 'POST':
        user = request.user

        user.company_name = request.POST.get('company_name')
        user.company_address = request.POST.get('main_location')
        user.company_email = request.POST.get('company_email')
        user.company_phone_number = request.POST.get('company_phone_number')
        user.company_description = request.POST.get('company_description')

        if 'logo_image' in request.FILES:
            if user.company_logo:
                user.company_logo.delete(save=False)  # Delete old image file
            user.company_logo = request.FILES['logo_image']
        
        user.save()
        
        messages.success(request, "Company profile updated successfully!")
        return redirect('employer_profile')
    return render(request,'employer_profile.html')

#for applicant verification request
@login_required
def applicant_verification_request(request):
    file_path = os.path.join(settings.BASE_DIR, 'data', 'ngolist.xlsx')
    df = pd.read_excel(file_path)

    # Get both name and email
    ngo_list = []
    for _, row in df.iterrows():
        name = row.iloc[0]
        email = row.iloc[1]
        if pd.notna(name) and pd.notna(email):
            ngo_list.append({'name': name, 'email': email})
    if request.method == 'POST':
        return redirect('applicant_verification_request')
    return render(request, 'applicant_verification_request.html', {'ngo_list': ngo_list})

#for change password form
@login_required
def change_password(request):
    return render(request, 'account_password_change.html')
