from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from . import models

class OnboardInstitute(forms.ModelForm):
    class Meta:
        model = models.DpyInstitute
        fields = ['name','institute_email','contact','board','nature','logo','school_image','university','address','city','pin_code','state',]

# class OnboardEmployee(forms.ModelForm):
#     class Meta:
#         model = models.DpyEmployee
#         fields = ['first_name','middle_name','last_name','email','mobile','image','type','designation',]
