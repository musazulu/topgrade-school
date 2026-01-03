from django.urls import path
from . import views

urlpatterns = [
    path('', views.enrollment_info, name='enrollment_info'),
    path('apply/', views.enrollment_apply, name='enrollment_apply'),
    path('apply/success/<uuid:application_id>/', views.enrollment_success, name='enrollment_success'),
    path('check-status/', views.check_status, name='check_status'),
]