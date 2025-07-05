from django.shortcuts import render,redirect
from django.contrib import messages

# Create your views here.

def view_job_table(request):
    return render(request,'advertisement_list.html')

def reload_job(request):
    if request.method == 'POST':
        return redirect('reload_job')
    return render(request, 'write.html')

def post_job(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'draft':
            messages.info(request, "Job saved as draft!")
        elif action == 'publish':
            messages.success(request, "Job Advertisement is Successfully Posted!")

        return redirect('view_job_table')
    return render(request, 'advertisement_list.html')
