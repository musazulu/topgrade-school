from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import EnrollmentApplication
from .forms import EnrollmentForm

def enrollment_info(request):
    """Enrollment information page"""
    return render(request, 'enrollment/info.html')

def enrollment_apply(request):
    """Online enrollment application"""
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            return redirect('enrollment_success', application_id=application.application_id)
    else:
        form = EnrollmentForm()
    
    return render(request, 'enrollment/apply.html', {'form': form})

def enrollment_success(request, application_id):
    """Application submission success page"""
    application = get_object_or_404(EnrollmentApplication, application_id=application_id)
    return render(request, 'enrollment/success.html', {'application': application})

def check_status(request):
    """Check application status"""
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        email = request.POST.get('email')
        
        try:
            application = EnrollmentApplication.objects.get(
                application_id=application_id,
                parent1_email=email
            )
            return render(request, 'enrollment/status.html', {'application': application})
        except EnrollmentApplication.DoesNotExist:
            return render(request, 'enrollment/status_check.html', {
                'error': 'Application not found. Please check your details.'
            })
    
    return render(request, 'enrollment/status_check.html')