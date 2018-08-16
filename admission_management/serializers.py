from .models import DpyInstituteAdmissionProspect
from rest_framework import serializers
# from admission_management.models import DpyInstituteAdmissionProspect
from .models import DpyInstituteAdmissionsUsers, DpyInstituteAdmissionProspect
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_auth.serializers import TokenSerializer
from rest_auth.models import TokenModel
from .models import DpyInstituteAdmissionsUsers
from onboarding.models import DpyInstitute, DpyUsers, DpyInstituteUsers
class InstituteAdmissionProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpyInstituteAdmissionProspect
        fields = ('name', 'email_id', 'phone_no', 'gender', 'course_id', 'admission_status')

class InstituteAdmissionsUsersSerializer(serializers.ModelSerializer):
	applicant_email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=DpyInstituteAdmissionsUsers.objects.all())])
	class Meta:
		model = DpyInstituteAdmissionsUsers
		fields = ('institute_id','institute_form_id','reg_no', 'first_name', 'middle_name', 'last_name', 'image', 'local_address','permanent_address','aadhar_no','fathers_name','mothers_name','dob','applicant_email','gender','applicant_phone','category_id','course_id','caste','parent_phone','parent_email','parent_occupation','annual_income','subject_content','form_content','nationality','status')