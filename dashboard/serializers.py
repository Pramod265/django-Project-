# from .models import DpyStudents
from rest_framework import serializers
from class_user_profiling.models import DpyInstituteUserClass,DpyInstituteClass,DpyInstituteAdditionalField
from onboarding.models import DpyInstitute, DpyInstituteUsers, DpyUsers

# class StudentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DpyStudents
#         fields = ('first_name', 'middle_name', 'last_name','email','mobile','dob','religion','caste','adhar_no','gender','blood_group')
