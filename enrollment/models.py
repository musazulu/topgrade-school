from django.db import models
from django.utils import timezone
import uuid

class EnrollmentApplication(models.Model):
    """Student enrollment application"""
    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('INTERVIEW_SCHEDULED', 'Interview Scheduled'),
        ('ACCEPTED', 'Accepted'),
        ('WAITLISTED', 'Waitlisted'),
        ('REJECTED', 'Rejected'),
        ('ENROLLED', 'Enrolled'),
    ]
    
    GRADE_CHOICES = [
        ('GRADE_1', 'Grade 1'),
        ('GRADE_2', 'Grade 2'),
        ('GRADE_3', 'Grade 3'),
        ('GRADE_4', 'Grade 4'),
        ('GRADE_5', 'Grade 5'),
        ('GRADE_6', 'Grade 6'),
    ]
    
    # Application Details
    application_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    intended_grade = models.CharField(max_length=20, choices=GRADE_CHOICES)
    intended_start_term = models.CharField(max_length=50)
    
    # Child Information
    child_first_name = models.CharField(max_length=100)
    child_last_name = models.CharField(max_length=100)
    child_dob = models.DateField()
    child_gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    child_nationality = models.CharField(max_length=100, blank=True)
    previous_school = models.CharField(max_length=200, blank=True)
    
    # Parent/Guardian Information
    parent1_name = models.CharField(max_length=100)
    parent1_relationship = models.CharField(max_length=50)
    parent1_email = models.EmailField()
    parent1_phone = models.CharField(max_length=20)
    parent1_occupation = models.CharField(max_length=100, blank=True)
    
    parent2_name = models.CharField(max_length=100, blank=True)
    parent2_relationship = models.CharField(max_length=50, blank=True)
    parent2_email = models.EmailField(blank=True)
    parent2_phone = models.CharField(max_length=20, blank=True)
    parent2_occupation = models.CharField(max_length=100, blank=True)
    
    # Address
    home_address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_relationship = models.CharField(max_length=50)
    emergency_contact_phone = models.CharField(max_length=20)
    
    # Medical Information
    allergies = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    doctor_name = models.CharField(max_length=100, blank=True)
    doctor_phone = models.CharField(max_length=20, blank=True)
    
    # Documents (file paths)
    birth_certificate = models.FileField(upload_to='enrollment/documents/', blank=True)
    previous_report = models.FileField(upload_to='enrollment/documents/', blank=True)
    immunization_record = models.FileField(upload_to='enrollment/documents/', blank=True)
    parent_id_copy = models.FileField(upload_to='enrollment/documents/', blank=True)
    photo = models.FileField(upload_to='enrollment/photos/', blank=True)
    
    # Additional Information
    how_did_you_hear = models.CharField(max_length=200, blank=True)
    additional_notes = models.TextField(blank=True)
    
    # Admin fields
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-application_date']
    
    def __str__(self):
        return f"{self.child_first_name} {self.child_last_name} - {self.get_status_display()}"
    
    def get_full_name(self):
        return f"{self.child_first_name} {self.child_last_name}"