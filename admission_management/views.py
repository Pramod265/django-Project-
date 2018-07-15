from django.shortcuts import render
from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from admission_management.serializers import InstituteAdmissionProspectSerializer
import json
from .models import DpyInstituteAdmissionProspect
from class_user_profiling.models import DpyInstituteClassSessionSubjectUser, DpyInstituteUserClass, DpyInstituteClass, DpyInstituteAdditionalField, DpyInstituteUserAdditionalField
from onboarding.models import DpyInstitute, DpyInstituteUsers
from onboarding.models import DpyUsers
def admission(request):
    return render(request,"admission_management/admission.html")

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