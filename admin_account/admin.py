from django.contrib import admin
from .models import CustomAdminUser

# Register your models here.
class CustomAdminUserAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'email', 'is_trusted']
    list_editable= ['is_trusted']
    list_filter = ['is_trusted', 'first_name']

admin.site.register(CustomAdminUser, CustomAdminUserAdmin)