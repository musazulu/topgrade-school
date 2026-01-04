from django.db import models
import uuid

class FeeStructure(models.Model):
    """School fee structure"""
    GRADE_CHOICES = [
        ('GRADE_1', 'Grade 1'),
        ('GRADE_2', 'Grade 2'),
        ('GRADE_3', 'Grade 3'),
        ('GRADE_4', 'Grade 4'),
        ('GRADE_5', 'Grade 5'),
        ('GRADE_6', 'Grade 6'),
    ]
    
    TERM_CHOICES = [
        ('TERM_1', 'Term 1'),
        ('TERM_2', 'Term 2'),
        ('TERM_3', 'Term 3'),
    ]
    
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)
    term = models.CharField(max_length=20, choices=TERM_CHOICES)
    academic_year = models.CharField(max_length=20)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    activity_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    technology_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    late_payment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['grade', 'term', 'academic_year']
    
    def __str__(self):
        return f"{self.get_grade_display()} - {self.get_term_display()} {self.academic_year}"
    
    def total_fee(self):
        return self.tuition_fee + self.activity_fee + self.technology_fee

class Payment(models.Model):
    """Payment records"""
    PAYMENT_METHOD_CHOICES = [
        ('CARD', 'Credit/Debit Card'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('MOBILE_MONEY', 'Mobile Money'),
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    student_name = models.CharField(max_length=200)
    parent_email = models.EmailField()
    application = models.ForeignKey('enrollment.EnrollmentApplication', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Fee details
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    # Payment details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True)
    
    # Dates
    payment_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(null=True, blank=True)
    
    # Bank transfer details
    bank_reference = models.CharField(max_length=100, blank=True)
    
    # Receipt
    receipt_number = models.CharField(max_length=50, blank=True)
    receipt_sent = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment {self.payment_id} - {self.student_name}"
    
    def generate_receipt_number(self):
        if not self.receipt_number:
            self.receipt_number = f"REC-{self.payment_date.strftime('%Y%m%d')}-{str(self.id).zfill(6)}"
            self.save()
        return self.receipt_number

class BankAccount(models.Model):
    """School bank account details"""
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=100, blank=True)
    branch_code = models.CharField(max_length=50, blank=True)
    swift_code = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"