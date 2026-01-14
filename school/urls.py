from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('staff/', views.staff_list, name='staff'),
    path('subjects/', views.subjects, name='subjects'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('enrollment/apply/', views.enrollment_form, name='enrollment_form'),
    path('enrollment/success/', views.enrollment_success, name='enrollment_success'),
    path('payments/bank-details/', views.bank_details, name='bank_details'),
    path('payments/fees/', views.fees_structure, name='fees'),
    path('payments/pay/', views.pay_at_office, name='pay_at_office'),
    path('uniforms/', views.uniforms, name='uniforms'),
    
]