from django import forms
from .models import EnrollmentApplication

class EnrollmentForm(forms.ModelForm):
    """Enrollment application form"""
    
    class Meta:
        model = EnrollmentApplication
        fields = [
            'intended_grade', 'intended_start_term',
            'child_first_name', 'child_last_name', 'child_dob', 'child_gender',
            'child_nationality', 'previous_school',
            'parent1_name', 'parent1_relationship', 'parent1_email', 'parent1_phone', 'parent1_occupation',
            'parent2_name', 'parent2_relationship', 'parent2_email', 'parent2_phone', 'parent2_occupation',
            'home_address', 'city', 'postal_code',
            'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone',
            'allergies', 'medications', 'medical_conditions', 'doctor_name', 'doctor_phone',
            'birth_certificate', 'previous_report', 'immunization_record', 'parent_id_copy', 'photo',
            'how_did_you_hear', 'additional_notes',
        ]
        
        widgets = {
            'child_dob': forms.DateInput(attrs={'type': 'date'}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
            'medications': forms.Textarea(attrs={'rows': 2}),
            'medical_conditions': forms.Textarea(attrs={'rows': 2}),
            'home_address': forms.Textarea(attrs={'rows': 3}),
            'additional_notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make some fields optional
        for field in ['parent2_name', 'parent2_relationship', 'parent2_email', 'parent2_phone',
                     'parent2_occupation', 'child_nationality', 'postal_code',
                     'doctor_name', 'doctor_phone']:
            self.fields[field].required = False