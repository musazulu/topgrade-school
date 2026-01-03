from django.contrib import admin
from django.utils import timezone  # ADD THIS IMPORT
from .models import SchoolInfo, StaffMember, Subject, Announcement, GalleryImage, ContactMessage, Enrollment, BankDetails

@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']
    
    def has_add_permission(self, request):
        # Only allow one school info record
        if self.model.objects.count() >= 1:
            return False
        return True

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'staff_type', 'grade_level', 'is_active']
    list_filter = ['staff_type', 'is_active']
    search_fields = ['name', 'position']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'display_order']
    list_filter = ['category']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_posted', 'is_active', 'display_on_homepage']
    list_filter = ['is_active', 'display_on_homepage']

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_active']
    list_filter = ['category', 'is_active']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'date_received', 'is_read']
    list_filter = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'child_age', 'message', 'date_received']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'grade_applying_for', 'parent_name', 'status', 'application_date']
    list_filter = ['status', 'grade_applying_for', 'gender']
    search_fields = ['first_name', 'last_name', 'parent_name', 'email']
    readonly_fields = ['application_date']
    fieldsets = (
        ('Student Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender')
        }),
        ('Contact Information', {
            'fields': ('parent_name', 'parent_relationship', 'email', 'phone', 'address')
        }),
        ('Academic Information', {
            'fields': ('grade_applying_for', 'previous_school', 'previous_grade')
        }),
        ('Special Information', {
            'fields': ('special_needs', 'additional_notes')
        }),
        ('Documents', {
            'fields': ('birth_certificate_provided', 'previous_report_provided', 'immunization_provided')
        }),
        ('Application Status', {
            'fields': ('status', 'reviewed_by', 'review_notes', 'review_date')
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Student Name'
    
    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and form.cleaned_data['status'] != 'PENDING':
            obj.reviewed_by = request.user
            obj.review_date = timezone.now()
        super().save_model(request, obj, form, change)

@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'account_number', 'is_active', 'last_updated']
    list_filter = ['is_active']