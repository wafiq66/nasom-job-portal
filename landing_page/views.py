from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

def landing_applicant(request):
    return render(request,"landing_applicant.html")

def landing_employer(request):
    return render(request,"landing_employer.html")

def view_job_ad(request):
    return render(request,'job_apply.html')

def view_applicant_recruit(request):
    return render(request,'applicant_recruit.html')

def hiring_advice(request):
    return render(request,'hiring_advice.html')

def search_company(request):
    return render(request,'search_company.html')

def view_company(request):
    return render(request,'view_company.html')