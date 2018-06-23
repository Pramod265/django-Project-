from django.shortcuts import render
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from onboarding.serializers import InstituteSerializer, InstituteUserSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

# from onboarding.models import DpyInstitute, DpyEmployee
from .models import DpyUsers
# from django.contrib.auth.hashers import make_password


# Create your views here.
# @api_view(['GET', 'POST'])
class SignUp(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        return render(request, 'onboarding/signup.html')

    def post(self, request, format=None):
        import json
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
