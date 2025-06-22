from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

def landing_applicant(request):
    return render(request,"landing_applicant.html")

def landing_employer(request):
    return render(request,"landing_employer.html")