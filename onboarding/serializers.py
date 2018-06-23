from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from onboarding.models import DpyInstitute, DpyUsers, DpyInstituteUsers


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpyInstitute
        # fields = ('id', 'name', 'institute_email', 'contact', 'board', 'nature', 'logo', 'school_image', 'university', 'address', 'city', 'pin_code', 'state', 'medium', 'country')
        fields = "__all__"


# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DpyEmployee
#         fields = ('id', 'first_name', 'middle_name', 'last_name', 'email', 'mobile', 'image', 'type', 'designation',)
#         # fields = "__all__"

def generate_username(first_name,last_name):
    val = "{0}.{1}_dmk".format(first_name[0],last_name).lower()
    tmp_val = "{0}.{1}".format(first_name[0],last_name).lower()
    x=0
    while True:
        if x == 0 and DpyUsers.objects.filter(username=val).count() == 0:
            return val
        else:
            new_val = "{0}{1}_dmk".format(tmp_val,x)
            if DpyUsers.objects.filter(username=new_val).count() == 0:
                return new_val
        x += 1
        if x > 1000000:
            raise Exception("Name is super popular!")


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=DpyUsers.objects.all())])
    # username = serializers.CharField(max_length=32,validators=[UniqueValidator(queryset=DpyUsers.objects.all())])
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        uname = generate_username(validated_data['first_name'],validated_data['last_name'])

        user = DpyUsers.objects.create_user(uname, validated_data['email'],validated_data['password'])
        if 'middle_name' in validated_data : user.middle_name = validated_data['middle_name']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.mobile = validated_data['mobile']
        user.save()
        
        return user

    class Meta:
        model = DpyUsers
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'email', 'mobile', 'image', 'password')
        extra_kwargs = {
            'last_login': {'read_only': True},
            'password': {'write_only': True}
        }

class InstituteUserSerializer(serializers.ModelSerializer):
    # users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    institute = InstituteSerializer(read_only=True)
    class Meta:
        model = DpyInstituteUsers
        fields = ('id', 'role', 'user', 'institute')
