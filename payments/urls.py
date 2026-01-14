from django.urls import path
from . import views
app_name = 'payments'    # in payments/urls.py

urlpatterns = [
    path('', views.payment_info, name='payment_info'),
    path('fees/', views.fee_structure, name='fee_structure'),
    path('pay/', views.make_payment, name='make_payment'),
    path('pay/process/', views.process_payment, name='process_payment'),
    path('pay/success/<uuid:payment_id>/', views.payment_success, name='payment_success'),
    path('bank-details/', views.bank_details, name='bank_details'),
]