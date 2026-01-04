from django.contrib import admin
from .models import EnrollmentApplication

@admin.register(EnrollmentApplication)
class EnrollmentApplicationAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'intended_grade', 'status', 'application_date']
    list_filter = ['status', 'intended_grade', 'application_date']
    search_fields = ['child_first_name', 'child_last_name', 'parent1_email', 'parent1_phone']
    readonly_fields = ['application_id', 'application_date']
    fieldsets = (
        ('Application Details', {
            'fields': ('application_id', 'status', 'intended_grade', 'intended_start_term')
        }),
        ('Child Information', {
            'fields': ('child_first_name', 'child_last_name', 'child_dob', 'child_gender',
                      'child_nationality', 'previous_school')
        }),
        ('Parent Information', {
            'fields': ('parent1_name', 'parent1_relationship', 'parent1_email', 'parent1_phone',
                      'parent2_name', 'parent2_relationship', 'parent2_email', 'parent2_phone')
        }),
        ('Address & Contacts', {
            'fields': ('home_address', 'city', 'postal_code',
                      'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone')
        }),
        ('Medical Information', {
            'fields': ('allergies', 'medications', 'medical_conditions', 'doctor_name', 'doctor_phone')
        }),
        ('Documents', {
            'fields': ('birth_certificate', 'previous_report', 'immunization_record', 'parent_id_copy', 'photo')
        }),
        ('Admin Section', {
            'fields': ('interview_date', 'interview_notes', 'admin_notes', 'how_did_you_hear', 'additional_notes'),
            'classes': ('collapse',)
        }),
    )