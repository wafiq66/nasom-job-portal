from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from verification_request.models import VerificationRequest

# Create your views here.
def verify_applicant(request,vr_id):
    verification = get_object_or_404(VerificationRequest, id=vr_id)

    if request.method == 'POST':
        ver_status = request.POST.get('action')
        ver_name = request.POST.get('verifier_name')
        ver_position = request.POST.get('verifier_position')
        ver_ngo_message = request.POST.get('verifier_message')

        verification.full_name = ver_name
        verification.position = ver_position
        verification.ngo_message = ver_ngo_message
        verification.verification_status = ver_status
        verification.verified_date = now()

        verification.save()
        
        return redirect('verify_applicant',vr_id)

    return render(request, 'verify_applicant.html',{
        'vr':verification,
    })