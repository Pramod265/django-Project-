# from .models import DpyStudents
from rest_framework import serializers
from class_user_profiling.models import DpyInstituteUserClass,DpyInstituteClass,DpyInstituteAdditionalField
from onboarding.models import DpyInstitute, DpyInstituteUsers, DpyUsers

class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = DpyUsers
		fields = ('first_name', 'middle_name', 'last_name','email','mobile','dob','religion','caste','adhar_no','gender','blood_group','mother_name','nationality','place_of_birth','address','address2','image')

class DpyInstituteUsersSerializer(serializers.ModelSerializer):
	
	first_name = serializers.CharField(source='user.first_name', read_only=True)
	middle_name = serializers.CharField(source='user.middle_name', read_only=True)
	last_name = serializers.CharField(source='user.last_name', read_only=True)
	batch_name = serializers.CharField(source='batch.name', read_only=True)
	date_joined = serializers.CharField(source='user.date_joined', read_only=True)
	email = serializers.CharField(source='user.email', read_only=True)
	mobile = serializers.CharField(source='user.mobile', read_only=True)
	dob = serializers.CharField(source='user.dob', read_only=True)
	gender = serializers.CharField(source='user.gender', read_only=True)
	blood_group = serializers.CharField(source='user.blood_group', read_only=True)
	religion = serializers.CharField(source='user.religion', read_only=True)
	caste = serializers.CharField(source='user.caste', read_only=True)
	mother_name = serializers.CharField(source='user.mother_name', read_only=True)
	nationality = serializers.CharField(source='user.nationality', read_only=True)
	place_of_birth = serializers.CharField(source='user.place_of_birth', read_only=True)
	address = serializers.CharField(source='user.address', read_only=True)
	address2 = serializers.CharField(source='user.address2', read_only=True)
	image = serializers.CharField(source='user.image', read_only=True)

	class Meta:
		model = DpyInstituteUsers
		fields = "__all__"