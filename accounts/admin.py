from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customuser
# Register your models here.
class Customuseradmin(UserAdmin):
    model = Customuser
    list_display =['username', 'email', 'first_name' , 'last_name', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'mobile_number', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'mobile_number', 'profile_picture')}),
    )
    
admin.site.register(Customuser,Customuseradmin)
