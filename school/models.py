from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Add this import at the top
class SchoolInfo(models.Model):
    """Core school information"""
    name = models.CharField(max_length=200, default="Top Grade Education Centre")
    motto = models.CharField(max_length=200, default="Excellence in Primary Education")
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=20, blank=True)
    operating_hours = models.CharField(max_length=100)
    
    # Mission & Values
    mission = models.TextField()
    vision = models.TextField(blank=True)
    
    # Social Media
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "School Information"

class StaffMember(models.Model):
    """School staff information"""
    STAFF_TYPE_CHOICES = [
        ('PRINCIPAL', 'Principal'),
        ('TEACHER', 'Teacher'),
        ('SUPPORT', 'Support Staff'),
        ('ADMIN', 'Administrative'),
    ]
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPE_CHOICES)
    bio = models.TextField(blank=True)
    qualifications = models.TextField(blank=True)
    photo = models.ImageField(upload_to='staff/', blank=True)
    email = models.EmailField(blank=True)
    phone_extension = models.CharField(max_length=10, blank=True)
    grade_level = models.CharField(max_length=50, blank=True, help_text="Grade(s) they teach")
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.position}"

class Subject(models.Model):
    """Subjects offered at the school"""
    CATEGORY_CHOICES = [
        ('CORE', 'Core Subject'),
        ('FOUNDATION', 'Foundation Subject'),
        ('SPECIAL', 'Special Program'),
        ('EXTRACURRICULAR', 'Extracurricular Activity'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'display_order']
    
    def __str__(self):
        return self.name

class Announcement(models.Model):
    """School announcements and news"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    display_on_homepage = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_posted']
    
    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    """School gallery images"""
    CATEGORY_CHOICES = [
        ('CLASSROOM', 'Classroom'),
        ('PLAYGROUND', 'Playground'),
        ('EVENT', 'School Event'),
        ('ACTIVITY', 'Learning Activity'),
        ('STAFF', 'Staff'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['category', 'display_order']
    
    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    """Messages from contact form"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    child_age = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    date_received = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_received']
    
    def __str__(self):
        return f"Message from {self.name}"
    

class Enrollment(models.Model):
    """Student enrollment application"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('REVIEWED', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('WAITLIST', 'Waitlisted'),
    ]
    
    GRADE_CHOICES = [
        ('GRADE_1', 'Grade 1'),
        ('GRADE_2', 'Grade 2'),
        ('GRADE_3', 'Grade 3'),
        ('GRADE_4', 'Grade 4'),
        ('GRADE_5', 'Grade 5'),
        ('GRADE_6', 'Grade 6'),
        ('GRADE_7', 'Grade 7'),
    ]
    
    # Student Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')])
    
    # Contact Information
    parent_name = models.CharField(max_length=200)
    parent_relationship = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    
    # Academic Information
    grade_applying_for = models.CharField(max_length=20, choices=GRADE_CHOICES)
    previous_school = models.CharField(max_length=200, blank=True)
    previous_grade = models.CharField(max_length=50, blank=True)
    
    # Special Information
    special_needs = models.TextField(blank=True, help_text="Any special educational needs, allergies, or medical conditions")
    additional_notes = models.TextField(blank=True)
    
    # Application Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    application_date = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    review_notes = models.TextField(blank=True)
    review_date = models.DateTimeField(null=True, blank=True)
    
    # Documents (you can later add file uploads)
    birth_certificate_provided = models.BooleanField(default=False)
    previous_report_provided = models.BooleanField(default=False)
    immunization_provided = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-application_date']
        verbose_name = "Enrollment Application"
        verbose_name_plural = "Enrollment Applications"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_grade_applying_for_display()}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def age_at_application(self):
        from datetime import date
        today = date.today()
        age = today.year - self.date_of_birth.year
        # Adjust if birthday hasn't occurred this year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

class BankDetails(models.Model):
    """Bank payment details for the school"""
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50)
    branch = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=20, blank=True)
    currency = models.CharField(max_length=50, default="KES")
    paybill_number = models.CharField(max_length=20, blank=True)
    instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Bank Details"
        verbose_name_plural = "Bank Details"
    
    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"
    
    def save(self, *args, **kwargs):
        # Ensure only one active bank details record exists
        if self.is_active:
            BankDetails.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)