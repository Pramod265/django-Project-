from django import forms
from . import models

class Students_reg_form(forms.ModelForm):
	class Meta:
		model = models.DpyStudents
		fields = '__all__'


class Student_update_form(forms.ModelForm):
	class Meta:
		model = models.DpyStudents
		fields = '__all__'	