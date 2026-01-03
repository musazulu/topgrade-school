from django import forms
from .models import ContactMessage, Enrollment
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'child_age', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class EnrollmentForm(forms.ModelForm):
    # Add custom validation
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Student's date of birth"
    )
    
    class Meta:
        model = Enrollment
        fields = [
            # Student Information
            'first_name', 'last_name', 'date_of_birth', 'gender',
            # Contact Information
            'parent_name', 'parent_relationship', 'email', 'phone', 'address',
            # Academic Information
            'grade_applying_for', 'previous_school', 'previous_grade',
            # Special Information
            'special_needs', 'additional_notes',
            # Documents
            'birth_certificate_provided', 'previous_report_provided', 'immunization_provided'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'special_needs': forms.Textarea(attrs={'rows': 3, 'placeholder': 'If none, leave blank'}),
            'additional_notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any additional information'}),
            'parent_relationship': forms.TextInput(attrs={'placeholder': 'e.g., Mother, Father, Guardian'}),
        }
        help_texts = {
            'previous_school': 'Name of previous school (if applicable)',
            'previous_grade': 'Most recent grade completed',
            'birth_certificate_provided': 'Check if birth certificate will be provided',
            'previous_report_provided': 'Check if previous school report will be provided',
            'immunization_provided': 'Check if immunization records will be provided',
        }
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            # Calculate age
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
            # Validate age for primary school (typically 5-13)
            if age < 5:
                raise forms.ValidationError("Student must be at least 5 years old for enrollment.")
            if age > 13:
                raise forms.ValidationError("For primary school enrollment, student should not be older than 13 years.")
        
        return dob
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if email already exists in pending applications
        if Enrollment.objects.filter(email=email, status='PENDING').exists():
            raise forms.ValidationError(
                "You already have a pending application with this email. "
                "Please wait for review or contact the school."
            )
        return email