from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from onboarding.models import DpyUsers

class DpyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = DpyUsers
        fields = ('username', 'email')

class DpyUserChangeForm(UserChangeForm):

    class Meta:
        model = DpyUsers
        fields = UserChangeForm.Meta.fields