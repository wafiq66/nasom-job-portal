from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from document.models import Document
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
    return render(request,'applicant_background.html')