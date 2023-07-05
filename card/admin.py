from django.contrib import admin
from .models import ExpertCard, CompanyAddress, ActivityLog

# Register your models here.
admin.site.register(ExpertCard)
admin.site.register(CompanyAddress)
admin.site.register(ActivityLog)
