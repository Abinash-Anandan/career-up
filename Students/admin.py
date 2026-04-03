from django.contrib import admin
from .models import EnrollmentRequest

@admin.register(EnrollmentRequest)
class EnrollmentRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'selected_path', 'email', 'phone_number', 'created_at', 'is_contacted')
    list_filter = ('selected_path', 'is_contacted', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number')
    date_hierarchy = 'created_at'
