from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User , OtpCode
from django.contrib.auth.models import Group
# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    readonly_fields = ('last_login',) #no one cant click this

    fieldsets =(
        (None,{'fields':('email', 'full_name', 'phone_number', 'password')}),
        ('Permissions' , {'fields': ('is_active', 'is_superuser','is_admin', 'last_login', 'groups', 'user_permissions')}),
    )

    add_fieldsets =(
        (None, {'fields':('phone_number','email', 'full_name', 'password1', 'password2')}),
    )

    search_fields =( 'email' , 'full_name')
    ordering =('full_name',)
   
    filter_horizontal = ('groups', 'user_permissions')

    
    def get_form(self, request, obj:None,**kwargs):           #gozineye tikiye is super user ro tooye admin panel kasi natoone vase khodesh ezane
        form= super().get_form(request, obj, **kwargs)
        is_superuser=request.user.is_superuser
        if not is_superuser:
            form.base_fields[is_superuser].disabled=True
        return form    



admin.site.register(User , UserAdmin)



@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')
    
