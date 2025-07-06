from django.shortcuts import render

# Create your views here.
def verify_applicant(request):
    return render(request, 'verify_applicant.html')