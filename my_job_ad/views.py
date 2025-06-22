from django.shortcuts import render

# Create your views here.

def view_job_table(request):
    return render(request,'advertisement_list.html')