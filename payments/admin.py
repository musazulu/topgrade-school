from django.contrib import admin
from .models import FeeStructure, Payment, BankAccount

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['grade', 'term', 'academic_year', 'tuition_fee', 'total_fee', 'is_active']
    list_filter = ['grade', 'term', 'academic_year', 'is_active']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'student_name', 'amount', 'payment_method', 'payment_status', 'payment_date']
    list_filter = ['payment_status', 'payment_method', 'payment_date']
    search_fields = ['student_name', 'parent_email', 'transaction_id']
    readonly_fields = ['payment_id', 'payment_date']

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'account_name', 'account_number', 'is_active']
    list_filter = ['is_active']