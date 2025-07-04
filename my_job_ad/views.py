from django.shortcuts import render,redirect

# Create your views here.

def view_job_table(request):
    return render(request,'advertisement_list.html')

def post_job(request):
    if request.method == 'POST':
        return redirect('post_job')
    return render(request, 'write.html')
