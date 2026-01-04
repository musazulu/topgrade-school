from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    """Payment form"""
    
    class Meta:
        model = Payment
        fields = ['student_name', 'parent_email', 'amount', 'description', 'payment_method']
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }