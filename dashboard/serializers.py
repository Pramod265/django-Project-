from .models import DpyStudents
from rest_framework import serializers


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpyStudents
        fields = ('first_name', 'middle_name', 'last_name','email','mobile','dob','religion','caste','adhar_no','gender','blood_group')
