from django import forms
from . import models
from onboarding.models import DpyUsers

# class Students_reg_form(forms.ModelForm):
# 	class Meta:
# 		model = models.DpyStudents
# 		fields = '__all__'


# class Student_update_form(forms.ModelForm):
# 	class Meta:
# 		model = models.DpyStudents
# 		fields = '__all__'	

# class Add_student(forms.ModelForm):
# 	class Meta:
# 		model = DpyUsers
# 		fields = '__all__'

from .models import Feedback
 
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['customer_name','email','details','phone_no', ]