from django import forms
from . import models

class Students_absenties_form(forms.ModelForm):
	class Meta:
		model = models.DpyStudentsAbsenties
		fields = '__all__'