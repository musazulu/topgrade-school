from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import FeeStructure, Payment, BankAccount
from .forms import PaymentForm

def payment_info(request):
    """Payment information page"""
    bank_accounts = BankAccount.objects.filter(is_active=True)
    return render(request, 'payments/info.html', {'bank_accounts': bank_accounts})

def fee_structure(request):
    """Fee structure display"""
    fees = FeeStructure.objects.filter(is_active=True).order_by('grade', 'term')
    return render(request, 'payments/fees.html', {'fees': fees})

def make_payment(request):
    """Initiate payment process"""
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.payment_status = 'PENDING'
            payment.save()
            
            if payment.payment_method == 'BANK_TRANSFER':
                return redirect('bank_details')
            else:
                payment.payment_status = 'COMPLETED'
                payment.save()
                return redirect('payment_success', payment_id=payment.payment_id)
    else:
        form = PaymentForm()
    
    return render(request, 'payments/make_payment.html', {'form': form})

def process_payment(request):
    """Process card payment"""
    return render(request, 'payments/process_payment.html')

def payment_success(request, payment_id):
    """Payment success page"""
    return render(request, 'payments/success.html', {'payment_id': payment_id})

def bank_details(request):
    """Bank transfer details"""
    bank_accounts = BankAccount.objects.filter(is_active=True)
    return render(request, 'payments/bank_details.html', {'bank_accounts': bank_accounts})