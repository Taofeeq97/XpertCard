# Django imports
from django.contrib import admin

# Local imports
from .models import ExpertCard, CompanyAddress, ActivityLog

# Register your models here.

class ExpertCardAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email','role', 'is_active', 'is_deleted']
    list_editable = ['is_active', 'is_deleted']
 

class CompanyAddressAdmin(admin.ModelAdmin):
    list_display = ['address_title', 'city', 'country', 'is_active', 'is_deleted']
    list_editable = ['is_active', 'is_deleted']

class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['actor','action_type', 'content_type', 'status', 'action_time']

admin.site.register(ExpertCard, ExpertCardAdmin)
admin.site.register(CompanyAddress, CompanyAddressAdmin)
admin.site.register(ActivityLog, ActivityLogAdmin)
