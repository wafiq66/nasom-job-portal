from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def applicant_list(request):
    if request.method == 'POST':
        return redirect('applicant_list')
    return render(request, 'applicant_list.html')

def applicant_manage(request):
    if request.method == 'POST':
        return redirect('applicant_manage')
    return render(request, 'applicant_manage.html')
