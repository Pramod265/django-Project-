from .models import DpyInstituteAdmissionProspect
from rest_framework import serializers
from admission_management.models import DpyInstituteAdmissionProspect
from .models import DpyInstituteAdmissionsUsers

class InstituteAdmissionProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpyInstituteAdmissionProspect
        fields = ('name', 'email_id', 'phone_no', 'gender', 'course_id', 'admission_status')

# class InstituteAdmissionsUsersSerializer(serializers.ModelSerializer):