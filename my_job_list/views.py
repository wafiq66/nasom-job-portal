from django.shortcuts import render

# Create your views here.
def saved_list(request):
    return render(request, 'saved_list.html')

def applied_list(request):
    return render(request, 'applied_list.html')