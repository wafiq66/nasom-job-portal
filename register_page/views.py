from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from application_user.models import ApplicationUser
from django.contrib import messages

def register(request):
    if request.method == "POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']

        if ApplicationUser.objects.filter(email=email).exists():
                    messages.error(request, "An account with this email already exists.")
                    return redirect("register_user")

        user = ApplicationUser(
            username = email,
            password = make_password(password),
            first_name = first_name,
            last_name = last_name,
            email = email,
        )

        user.save()
        
        messages.success(request, "Account created successfully.")

        return redirect("register_user")
    return render(request, 'register.html')
