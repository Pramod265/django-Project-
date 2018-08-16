from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .forms import DpyUserCreationForm, DpyUserChangeForm
from onboarding.models import DpyUsers

class CustomUserAdmin(UserAdmin):
    add_form = DpyUserCreationForm
    form = DpyUserChangeForm
    model = DpyUsers
    list_display = ['email', 'username', 'mobile', ]

admin.site.register(DpyUsers, CustomUserAdmin)