from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        

        if user is not None:
            login(request, user)
            accountType = request.POST['account_type']
            if accountType == 'applicant':
                return redirect("landing_applicant")
            
            else:
                return redirect('landing_employer')
            
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login_user")

    return render(request, 'login.html')


# Create your views here.
