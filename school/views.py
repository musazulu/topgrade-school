from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import SchoolInfo, StaffMember, Subject, Announcement, GalleryImage, ContactMessage
from .forms import ContactForm
from .forms import EnrollmentForm
from django.core.mail import send_mail
from django.conf import settings

from .models import Enrollment

def home(request):
    """Homepage view"""
    announcements = Announcement.objects.filter(is_active=True, display_on_homepage=True)[:3]
    school_info = SchoolInfo.objects.first()
    
    context = {
        'announcements': announcements,
        'school_info': school_info,
    }
    return render(request, 'school/home.html', context)

def about(request):
    """About page view"""
    school_info = SchoolInfo.objects.first()
    return render(request, 'school/about.html', {'school_info': school_info})

def staff_list(request):
    """Staff listing view"""
    staff = StaffMember.objects.filter(is_active=True).order_by('staff_type', 'display_order')
    
    # Group by staff type
    staff_by_type = {}
    for member in staff:
        staff_type = member.get_staff_type_display()
        if staff_type not in staff_by_type:
            staff_by_type[staff_type] = []
        staff_by_type[staff_type].append(member)
    
    return render(request, 'school/staff.html', {'staff_by_type': staff_by_type})

def subjects(request):
    """Subjects page view - GET FROM DATABASE"""
    print("🔍 DEBUG: Subjects view called")
    
    try:
        # Get all subjects from database, ordered properly
        subjects_list = Subject.objects.all().order_by('category', 'display_order')
        
        # DEBUG: Print what we're getting from database
        print(f"🔍 DEBUG: Found {subjects_list.count()} subjects in database")
        for subject in subjects_list:
            print(f"  - ID: {subject.id}, Name: {subject.name}, Category: {subject.category}, Display: {subject.get_category_display()}")
        
        # Group by category for template
        subjects_by_category = {}
        for subject in subjects_list:
            # Use the display value from choices
            category_display = subject.get_category_display()
            print(f"🔍 DEBUG: Processing subject '{subject.name}' -> category_display: '{category_display}'")
            
            if category_display not in subjects_by_category:
                subjects_by_category[category_display] = []
                print(f"🔍 DEBUG: Created new category list for '{category_display}'")
            
            # Add subject with all its attributes
            subjects_by_category[category_display].append({
                'id': subject.id,
                'name': subject.name,
                'description': subject.description,
                'icon_class': subject.icon_class,
                'display_order': subject.display_order,
                'category': subject.category,
                'category_display': category_display,
            })
            print(f"🔍 DEBUG: Added '{subject.name}' to category '{category_display}'")
        
        print(f"🔍 DEBUG: Final subjects_by_category keys: {list(subjects_by_category.keys())}")
        
        context = {
            'subjects_by_category': subjects_by_category,
            'has_subjects': subjects_list.exists()
        }
        
        return render(request, 'school/subjects.html', context)
        
    except Exception as e:
        print(f"❌ Error in subjects view: {e}")
        import traceback
        traceback.print_exc()
        # Fallback to sample data
        return render(request, 'school/subjects.html', {
            'subjects_by_category': get_sample_subjects(),
            'has_subjects': False,
            'error': str(e)
        })
def gallery(request):
    """Gallery page view"""
    images = GalleryImage.objects.filter(is_active=True).order_by('category', 'display_order')
    
    # Group by category
    images_by_category = {}
    for image in images:
        category = image.get_category_display()
        if category not in images_by_category:
            images_by_category[category] = []
        images_by_category[category].append(image)
    
    return render(request, 'school/gallery.html', {'images_by_category': images_by_category})

def contact(request):
    """Contact page view"""
    school_info = SchoolInfo.objects.first()
    form = ContactForm()
    return render(request, 'school/contact.html', {
        'school_info': school_info,
        'form': form
    })


def contact_submit(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send confirmation email to user
            subject = f'Message Received - Top Grade Education Centre'
            message = f"""
            Dear {contact_message.name},
            
            Thank you for contacting Top Grade Education Centre.
            We have received your message and will respond within 24-48 hours.
            
            Your Message Details:
            - Reference: {contact_message.id}
            - Date: {contact_message.date_received.strftime('%B %d, %Y at %I:%M %p')}
            - Subject: General Inquiry
            
            If you need immediate assistance, please call us at (020) 123-4567.
            
            Best regards,
            Top Grade Education Centre Team
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [contact_message.email],
                    fail_silently=False,
                )
            except:
                # If email fails, still show success page
                pass
            
            return render(request, 'school/contact_success.html', {
                'contact_message': contact_message
            })
    return redirect('contact')
def enrollment_form(request):
    """Display enrollment form"""
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.save()
            
            # In a real application, you would send an email here
            # send_enrollment_confirmation_email(enrollment)
            
            return render(request, 'school/enrollment_success.html', {
                'email': enrollment.email,
                'application_id': enrollment.id,
                'submission_date': enrollment.application_date.strftime('%B %d, %Y at %I:%M %p')
            })
    else:
        form = EnrollmentForm()
    
    return render(request, 'school/enrollment_form.html', {'form': form})

def enrollment_success(request):
    """Success page after enrollment submission"""
    return render(request, 'school/enrollment_success.html')


def bank_details(request):
    """Display bank payment details"""
    try:
        bank_details_obj = BankDetails.objects.filter(is_active=True).first()
        if bank_details_obj:
            bank_details = {
                'bank_name': bank_details_obj.bank_name,
                'account_name': bank_details_obj.account_name,
                'account_number': bank_details_obj.account_number,
                'branch': bank_details_obj.branch,
                'swift_code': bank_details_obj.swift_code,
                'currency': bank_details_obj.currency,
                'paybill_number': bank_details_obj.paybill_number,
            }
        else:
            bank_details = {}
    except:
        bank_details = {}
    
    return render(request, 'payments/bank_details.html', {'bank_details': bank_details})

def fees_structure(request):
    """Display school fees structure"""
    # You can add dynamic fees from database later
    context = {
        'academic_year': '2024',
        'last_updated': 'January 2024',
    }
    return render(request, 'payments/fees.html', context)

def pay_at_office(request):
    """Display information about paying at office"""
    context = {
        'office_location': 'Top Grade Education Centre, 123 Learning Street, Education Zone, Nairobi',
        'contact_numbers': ['(020) 123-4567', '0712 345 678', '0700 123 456'],
        'email': 'accounts@topgrade.edu',
    }
    return render(request, 'payments/pay_at_office.html', context)