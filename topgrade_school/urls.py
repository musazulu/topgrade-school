"""
URL configuration for topgrade_school project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include(("school.urls", "school"), namespace="school")),

    # Enrollment URLs
    path("enrollment/", include(("enrollment.urls", "enrollment"), namespace="enrollment")),

    # Payments URLs
    path("payments/", include(("payments.urls", "payments"), namespace="payments")),

    # Accounts URLs (no namespace shown in your code)
    path("accounts/", include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
