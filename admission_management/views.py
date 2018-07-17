from django.shortcuts import render
from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from admission_management.serializers import InstituteAdmissionProspectSerializer
import json
from django.views.decorators.csrf import csrf_exempt
from .models import DpyInstituteAdmissionProspect
from class_user_profiling.models import DpyInstituteClassSessionSubjectUser, DpyInstituteUserClass, DpyInstituteClass, DpyInstituteAdditionalField, DpyInstituteUserAdditionalField
from .serializers import InstituteAdmissionsUsersSerializer
from onboarding.models import DpyInstitute, DpyInstituteUsers
from onboarding.models import DpyUsers
from onboarding.serializers import InstituteUserSerializer, UserSerializer

class Admission(APIView):
    # permission_classes = (AllowAny,)
    def get(self, request, format=None):
        queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
        serializer = InstituteUserSerializer(queryset)
        InstUserid = (serializer.data["id"])
        InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
        institute_id = InstUser.institute_id
        print(institute_id)
        total_classes = DpyInstituteClass.objects.all().filter(institute_id = institute_id)
        return render(request,"admission_management/admission.html",{'total_classes':total_classes,'institute_id':institute_id})

    @csrf_exempt
    def post(self,request, format=None):
        userSerial = InstituteAdmissionsUsersSerializer(data=json.loads(request.data.get('user')))
        if userSerial.is_valid():
            user = userSerial.save()
            if request.FILES.get('image') is not None : user.image = request.FILES.get('image')
            user.created_by = request.user.id
            user.save()
            return Response({"status": True, "message": "Applied Successfully."}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": userSerial.errors}, status=status.HTTP_400_BAD_REQUEST)

def enquiry(request):
    print(request.session['institute_id'])
    total_classes = DpyInstituteClass.objects.all().filter(institute_id=request.session['institute_id'])
    return render(request, 'admission_management/enquiry.html',{'total_classes':total_classes})



def view_enquiry(request):
    if request.method == 'GET':
         queryset = DpyInstituteAdmissionProspect.objects.filter(institute_id = 1)
         serializer = InstituteAdmissionProspectSerializer(queryset, many=True)
    return render(request,"admission_management/view_enquiry.html",{'enquiry':serializer.data})
    


def view_admission(request):
    return render(request,"admission_management/view_admission.html")


def take_enquiry(request):
    if request.method == 'POST':
        enquiryData = request.POST.getlist('enquiryData[]')
        enquiry = DpyInstituteAdmissionProspect()
        enquiry.institute_id_id  = 1#request.session['institute_id']
        enquiry.name  = enquiryData[0]
        enquiry.email_id  = enquiryData[1]
        enquiry.phone_no  = enquiryData[2]
        enquiry.gender  = enquiryData[3]
        enquiry.course_id = enquiryData[5]
        enquiry.admission_status  = enquiryData[4]
        enquiry.save()
        response_data ={'Status':True, 'Message':'done'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")   
    return render(request,"admission_management/enquiry.html",{'form':[]})


# def view_enquiry_details(request,id):
    # try:
    #     queryset = DpyInstituteAdmissionProspect.objects.get(pk=id)
    # except DpyInstituteAdmissionProspect.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    # if request.method == 'GET':
    #     serializer = InstituteAdmissionProspectSerializer(queryset)
    #     return render(request,"admission_management/view_enquiry_details.html",{'data':serializer.data})