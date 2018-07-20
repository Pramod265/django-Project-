from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from onboarding.serializers import InstituteSerializer, InstituteUserSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from class_user_profiling.models import DpyInstituteClassSessionSubjectUser, DpyInstituteUserClass, DpyInstituteClass, DpyInstituteAdditionalField, DpyInstituteUserAdditionalField
from .models import DpyUsers, DpyInstitute, DpyInstituteUsers
# from onboarding.models import DpyInstitute, DpyEmployee
# from django.contrib.auth.hashers import make_password
import json


# @api_view(['GET', 'POST'])
class SignUp(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        return render(request, 'onboarding/signup.html')

    def post(self, request, format=None):
        institute = InstituteSerializer(data=json.loads(request.data.get('institute')))
        if institute.is_valid():
            userSerial = UserSerializer(data=json.loads(request.data.get('user')))
            if userSerial.is_valid():
                instUser = InstituteUserSerializer(data=json.loads(request.data.get('instuser')))
                if instUser.is_valid():
                    user = userSerial.save()
                    # if request.FILES.get('image') is not None : user.image = request.FILES.get('image')
                    # user.created_by = user.id
                    # user.save()

                    instData = {"created_by":user.pk}
                    # if request.FILES.get('logo') is not None : instData['logo'] = request.FILES.get('logo')
                    # if request.FILES.get('school_image') is not None : instData['school_image'] = request.FILES.get('school_image')
                    inst = institute.save(**instData)
                    
                    instUserdata = {"created_by":user.pk, "user_id":user.pk, "institute_id":inst.id}
                    instUser.save(**instUserdata)

                    return Response({"status": True, "message": "Created Successfully."}, status=status.HTTP_201_CREATED)
                return Response({"status": False, "message": instUser.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": False, "message": userSerial.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": False, "message": institute.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddTeacher(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        return render(request, 'onboarding/add-teacher.html')

    def post(self, request, format=None):
        import json
        userSerial = UserSerializer(data=json.loads(request.data.get('user')))
        if userSerial.is_valid():
            instUser = InstituteUserSerializer(data=json.loads(request.data.get('instuser')))
            if instUser.is_valid():
                user = userSerial.save()
                if request.FILES.get('image') is not None : user.image = request.FILES.get('image')
                user.created_by = request.user.id
                user.save()

                instUserdata = {"created_by":request.user.id, "user_id":user.pk, "institute_id":request.session['institute_id']}
                instUser.save(**instUserdata)

                return Response({"status": True, "message": "Created Successfully."}, status=status.HTTP_201_CREATED)
            return Response({"status": False, "message": instUser.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": False, "message": userSerial.errors}, status=status.HTTP_400_BAD_REQUEST)

from django.views.decorators.csrf import csrf_exempt

class AddStudent(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
        serializer = InstituteUserSerializer(queryset)
        InstUserid = (serializer.data["id"])
        InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
        inst_class = DpyInstituteClass.objects.all().filter(institute_id = InstUser.institute_id)
        AdditionFields = DpyInstituteAdditionalField.objects.all().filter(institute_id = InstUser.institute_id)
        
        return render(request, 'dashboard/add_students.html',{'inst_class':inst_class,'AdditionFields':AdditionFields})
    @csrf_exempt
    def post(self, request, format=None):
        queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
        serializer = InstituteUserSerializer(queryset)
        InstUserid = (serializer.data["id"])
        InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
        inst_class = DpyInstituteClass.objects.all().filter(institute_id = InstUser.institute_id)
        AdditionFields = DpyInstituteAdditionalField.objects.all().filter(institute_id = InstUser.institute_id)
        import json
        
        userSerial = UserSerializer(data=json.loads(request.data.get('user')))
        if userSerial.is_valid():
            instUser = InstituteUserSerializer(data=json.loads(request.data.get('instuser')))
            if instUser.is_valid():
                user = userSerial.save()
                if request.FILES.get('image') is not None : user.image = request.FILES.get('image')
                user.created_by = request.user.id
                user.save()

                instUserdata = {"created_by":request.user.id, "user_id":user.pk, "institute_id": InstUser.institute_id}
                instUser.save(**instUserdata)

                
                class_user = json.loads(request.data.get('class_user'))
                user_class = DpyInstituteUserClass(user_type=1,roll_no=class_user['roll_no'],status=1,created_by=request.user.id,ic_id=class_user['selected_class'],user_id=user.pk)
                user_class.save()

                
                additional_fields = json.loads(request.data.get('additional_fields'))
                for field in AdditionFields:
                    add_field = DpyInstituteUserAdditionalField(value = additional_fields[field.key_name],status=1,created_by=request.user.id,updated_by=0,iaf_id=field.id,user_id=user.pk)
                    add_field.save()

                return Response({"status": True, "message": "Created Successfully."}, status=status.HTTP_201_CREATED)
            return Response({"status": False, "message": instUser.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": False, "message": userSerial.errors}, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='/')
@api_view(['GET'])
def get_institute_teachers(request):
    if request.user.is_authenticated:
        from django.core import serializers

        queryset = DpyInstituteUsers.objects.filter(institute_id=request.session['institute_id'],type=2).defer("updated_on","updated_by","status")
        data = json.loads(serializers.serialize('json', queryset, fields=['designation','type','date_of_joining','user','institute_user_id','role','institute','date_of_leaving']))
        user_id = list(map(lambda x: x["fields"]["user"], data))#[(u['fields']['user']) for u in enumerate(data)]
        queryset2 = DpyUsers.objects.filter(pk__in=user_id).defer("updated_on","updated_by","status")
        data1 = json.loads(serializers.serialize('json', queryset2,fields=['first_name','middle_name', 'last_name', 'email', 'mobile', 'image','dob','gender','blood_group','religion','caste','nationality','place_of_birth','address','address2']))

        final_data = {}
        for value in data1:
            value['fields']['user_id'] = value['pk']
            final_data.setdefault(value['pk'], {}).update(value["fields"])

        for value in data:
            value['fields']['institute_user_id'] = value['pk']
            final_data[value['fields']['user']].update({'institute_user':value['fields']})

        return Response({"status": True, "message": "Data found Successfully.",'data':final_data})
    return redirect('login_view')
