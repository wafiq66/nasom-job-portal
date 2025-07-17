from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from job_ad.models import JobAd
from django.utils.timezone import now

# Create your views here.

def view_job_table(request):
    job_ads = JobAd.objects.filter(user=request.user)
    return render(request,'advertisement_list.html',{'job_ads':job_ads})

def reload_job(request,job_id):
    job_ad = get_object_or_404(JobAd, id=job_id, user = request.user)
    return render(request, 'write.html', {'job_ad':job_ad})


#bahagian ini adalah bahagian coding untuk alpha sigma post job
#dan juga digunakan untuk update job ad
def post_job(request):
    if request.method == 'POST':

        #read the button 
        action = request.POST.get('action')

        #use to create the class of JobAd or call the class JobAd
        jobad_id = request.POST.get("jobad_id")

        if jobad_id not in [None, ""]:
            job_ad = JobAd.objects.get(id=jobad_id)
        else:
            job_ad = JobAd()

        job_ad.user = request.user

        # Basic Info
        job_ad.job_title = request.POST.get("jobtitle", "")
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        job_ad.job_location = f"{city}, {state}" if city and state else city or state
        job_ad.for_level_one = bool(request.POST.get("autism-level-1"))
        job_ad.for_level_two = bool(request.POST.get("autism-level-2"))
        job_ad.for_level_three = bool(request.POST.get("autism-level-3"))

        # Category & Type
        job_ad.job_category = request.POST.get("job-category")
        job_ad.can_full_time = bool(request.POST.get("full-time"))
        job_ad.can_part_time = bool(request.POST.get("part-time"))
        job_ad.can_remote = bool(request.POST.get("remote"))

        # Salary
        job_ad.minimum_salary = request.POST.get("min-pay") or None
        job_ad.maximum_salary = request.POST.get("max-pay") or None

        # Tasks
        job_ad.main_task_desc = request.POST.get("maintask")
        job_ad.sub_task_status = bool(request.POST.get("toggleSubtaskStatus"))
        job_ad.sub_task_desc = request.POST.get("subtask")

        job_ad.repetitive_task_status = bool(request.POST.get("repetitiveTask"))
        job_ad.easy_to_perform_status = bool(request.POST.get("easyToPerform"))
        job_ad.easy_to_remember_status = bool(request.POST.get("easyToRemember"))

        # Interaction
        job_ad.interaction_with_cust_status = bool(request.POST.get("toggleInteractionWithCustomerStatus"))
        job_ad.interaction_with_cust_desc = request.POST.get("interactionWithCustomer")

        # Interview Approach
        job_ad.verbal_interview_status = bool(request.POST.get("toggleVerbalStatus"))
        job_ad.verbal_interview_desc = request.POST.get("verbal")

        job_ad.nonverbal_interview_status = bool(request.POST.get("toggleNonVerbalStatus"))
        job_ad.nonverbal_interview_desc = request.POST.get("nonverbal")

        job_ad.representative_interview_status = bool(request.POST.get("toggleRepresentativeStatus"))
        job_ad.representative_interview_desc = request.POST.get("representative")

        job_ad.no_interview_status = bool(request.POST.get("noInterview"))

        # Benefits
        job_ad.special_training_status = bool(request.POST.get("toggleSpecialTrainingStatus"))
        job_ad.special_training_desc = request.POST.get("specialTraining")

        job_ad.work_buddy_status = bool(request.POST.get("toggleWorkBuddyStatus"))
        job_ad.work_buddy_desc = request.POST.get("workBuddy")

        job_ad.mentor_status = bool(request.POST.get("toggleMentorStatus"))
        job_ad.mentor_desc = request.POST.get("mentor")

        job_ad.calming_space_status = bool(request.POST.get("toggleCalmingSpaceStatus"))
        job_ad.calming_space_desc = request.POST.get("calmingSpace")

        job_ad.less_noisy_env_status = bool(request.POST.get("lessNoisy"))
        job_ad.less_stressful_env_status = bool(request.POST.get("lessStressful"))

        job_ad.regular_update_status = bool(request.POST.get("toggleProgressUpdateStatus"))
        job_ad.regular_update_desc = request.POST.get("progressUpdate")

        # Training Frequency (radio)
        training_time = request.POST.get("training-time")
        job_ad.one_training_status = training_time == "one"
        job_ad.multiple_training_status = training_time == "multiple"
        job_ad.time_training_desc = request.POST.get("training-description")

        # Shift Arrangement (radio)
        shift = request.POST.get("shift-arrangement")
        job_ad.full_flexible_status = shift == "flexible"
        job_ad.shift_pool_status = shift == "pool"
        job_ad.shift_flexicle_desc = request.POST.get("shift-description")

        # Transportation (radio)
        transport = request.POST.get("transportation")
        job_ad.full_transport_status = transport == "full"
        job_ad.partial_transport_status = transport == "partial"
        job_ad.transport_desc = request.POST.get("transportation-description")

        # Other Notes
        job_ad.other_status = bool(request.POST.get("toggleOtherNotesStatus"))
        job_ad.other_desc = request.POST.get("otherNotes")

        # Pre-Interview Questions
        job_ad.question_one = request.POST.get("question1")
        job_ad.question_two = request.POST.get("question2")
        job_ad.question_three = request.POST.get("question3")

        # Publishing
        job_ad.publish_status = action or "draft"
        job_ad.publish_date = now()

        # Log to backend
        print("JobAd object preview:", job_ad.__dict__)

        if action == 'draft':
            messages.info(request, "Job saved as draft!")
        elif action == 'active':
            messages.success(request, "Job Advertisement is Successfully Posted!")
        job_ad.save()

        return redirect('view_job_table')
    return render(request, 'write.html')

#this one function untuk delete the job ad
def close_job(request,job_id):
    myJobAd = get_object_or_404(JobAd,id=job_id,user=request.user)
    myJobAd.publish_status = 'expired'
    myJobAd.save()
    messages.success(request, "Job Advertisement is Successfully Closed!")
    return redirect('view_job_table')

def delete_job(request,job_id):
    myJobAd = get_object_or_404(JobAd, id=job_id,user=request.user)
    myJobAd.delete()
    messages.success(request, "Job Advertisement is Successfully Deleted!")
    return redirect('view_job_table')

def republish_job(request,job_id):
    myJobAd = get_object_or_404(JobAd,id=job_id,user=request.user)
    myJobAd.publish_status = 'active'
    myJobAd.save()
    messages.success(request, "Job Advertisement is Successfully Republished!")
    return redirect('view_job_table')