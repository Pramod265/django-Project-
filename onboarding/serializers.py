from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_auth.serializers import TokenSerializer
from rest_auth.models import TokenModel
from onboarding.models import DpyInstitute, DpyUsers, DpyInstituteUsers


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpyInstitute
        fields = ('id', 'name', 'institute_email', 'contact', 'board', 'nature', 'logo', 'institute_image', 'university', 'address', 'city', 'pin_code', 'state', 'medium', 'country')

# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DpyEmployee
#         fields = ('id', 'first_name', 'middle_name', 'last_name', 'email', 'mobile', 'image', 'type', 'designation',)
#         # fields = "__all__"

def generate_username(first_name,last_name):
    val = "{0}.{1}_dmk".format(last_name[0],first_name).lower()
    tmp_val = "{0}.{1}".format(last_name[0],first_name).lower()
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
    password = serializers.CharField(min_length=3)

    def create(self, validated_data):
        uname = generate_username(validated_data['first_name'],validated_data['last_name'])

        user = DpyUsers.objects.create_user(uname, validated_data['email'],validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.mobile = validated_data['mobile']
        if 'middle_name' in validated_data : user.middle_name = validated_data['middle_name']
        if 'dob' in validated_data : user.dob = validated_data['dob']
        if 'gender' in validated_data : user.gender = validated_data['gender']
        else: user.gender = None
        if 'blood_group' in validated_data : user.blood_group = validated_data['blood_group']
        if 'religion' in validated_data : user.religion = validated_data['religion']
        if 'caste' in validated_data : user.caste = validated_data['caste']
        if 'nationality' in validated_data : user.nationality = validated_data['nationality']
        if 'place_of_birth' in validated_data : user.place_of_birth = validated_data['place_of_birth']
        if 'address' in validated_data : user.address = validated_data['address']
        if 'address2' in validated_data : user.address2 = validated_data['address2']
        if 'mother_name' in validated_data : user.mother_name = validated_data['mother_name']
        user.save()
        
        return user

    class Meta:
        model = DpyUsers
        fields = ('id', 'first_name', 'middle_name', 'last_name','mother_name' ,'email', 'mobile', 'image', 'password','dob','gender','blood_group','religion','caste','nationality','place_of_birth','address','address2')
        extra_kwargs = {
            'last_login': {'read_only': True},
            'password': {'write_only': True}
        }


class InstituteUserSerializer(serializers.ModelSerializer):
    institute = serializers.SerializerMethodField()#InstituteSerializer(read_only=True)

    def get_institute(self, obj):
        queryset = DpyInstitute.objects.get(pk=obj.institute_id)
        inst_details = InstituteSerializer(queryset,read_only=True)
        return inst_details.data

    class Meta:
        model = DpyInstituteUsers
        fields = ('id', 'institute_id', 'user_id', 'type', 'role', 'designation', 'date_of_joining', 'institute', )


class UserDetails(serializers.ModelSerializer):
    # token = serializers.SerializerMethodField()
    institute_info = serializers.SerializerMethodField()
    user = UserSerializer()

    def get_institute_info(self, obj):
        inst_id = self.context.get('institute_id')
        if inst_id:
            queryset = DpyInstituteUsers.objects.filter(user_id = obj.user_id,institute_id=inst_id)
            user_details = InstituteUserSerializer(queryset,many=True,read_only=True)
        else:
            queryset = DpyInstituteUsers.objects.filter(user_id = obj.user_id)
            user_details = InstituteUserSerializer(queryset,many=True,read_only=True)
        return user_details.data

    # def get_token(self, obj):
    #     queryset = TokenModel.objects.get(user_id = obj.id)
    #     user_details = TokenSerializer(queryset,read_only=True)
    #     return user_details.data        

    class Meta:
        model = TokenModel
        # fields = ('id', 'first_name', 'middle_name', 'last_name', 'email', 'mobile', 'image', 'password', 'last_login', 'token', 'institute_info', )
        fields = ('key', 'user', 'institute_info', )