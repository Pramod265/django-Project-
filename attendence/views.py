from django.http import HttpResponse,HttpResponseRedirect
from dashboard.models import DpyStudents
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .models import DpyStudentsAbsenties
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from onboarding.models import DpyInstitute, DpyInstituteUsers, DpyUsers
from onboarding.serializers import InstituteUserSerializer
import json, datetime
# Create your views here.

from django.views.decorators.csrf import csrf_exempt
@login_required(login_url='/')
@csrf_exempt

def take_attendence(request):
    queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
    serializer = InstituteUserSerializer(queryset)
    InstUserid = (serializer.data["id"])
    InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
    InstUserarr = ['role','designation','date_of_joining','is_active','status','institute_id','user_id'] 
    if request.method == 'GET':
        students = DpyStudents.objects.all().filter(institute_id = InstUser.institute_id).order_by('student_class','section')
        section_class = []
        counter = 0
        # for i in range(0,len(section_class)):
        #         student_class_section = student.student_class +" "+ student.section
        #         if section_class[i] is student_class_section:
        #             # break
        #             pass
        #         # if i == len(section_class):
        #         #     section_class[i] = student.student_class+" "+student.section
        # # print(students.student_class)
        for student in students:
            student_class = student.student_class
            student_section =student.section
            student_class_section = student_class +" "+ student_section
            if student_class_section in section_class:
                continue
            print(student_class_section)
            section_class.append(student_class_section)

        return render(request,'attendence/take_attendence.html',{'section_class':section_class})
    if request.method == 'POST':
        student_class_section = request.POST.get('student_class')
        student_class = student_class_section[:-2]
        section = student_class_section[-1:]
        print(student_class)
        print(section)
        students = DpyStudents.objects.all().filter(institute_id = InstUser.institute_id , student_class = student_class, section = section)
        # print(students)
        # view_students_for_attendence(request,student_class,section)    
        # return HttpResponseRedirect(request,"attendence:take_attendence",{'students':students})
        return render(request,"attendence/take_attendence.html",{'students':students})
    
# def view_students_for_attendence(request,student_class=None,section=None):
#     queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
#     serializer = InstituteUserSerializer(queryset)
#     InstUserid = (serializer.data["id"])
#     InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
#     InstUserarr = ['role','designation','date_of_joining','is_active','status','institute_id','user_id'] 
    
#     students = DpyStudents.objects.all().filter(institute_id = InstUser.institute_id , student_class = student_class, section = section)
#     return render(request,"attendence/take_attendence.html",{'students':students})
from .forms import Students_absenties_form
@login_required(login_url='/')
@csrf_exempt
def apply_attendence(request):
    if request.method == 'POST':
        
        # queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
        # serializer = InstituteUserSerializer(queryset)
        # InstUserid = (serializer.data["id"])
        # InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
                
        formData = request.POST.getlist('formData[]')
        
        for i in range(0,len(formData)):
            stud_id = formData[i]
            attendence_date =str(datetime.date.today())
            # array = [attendence_date,formData[i],request.user.id]
            # form = Students_absenties_form(array)
            # form.save()
            form = DpyStudentsAbsenties(date=attendence_date,student_id=stud_id,teacher_id=request.user.id,status=1)
            form.save()
        response_data ={'Status':True, 'Message': attendence_date }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    student = DpyStudents.objects.get(id=id)
    return render(request,'dashboard/student_profile.html',{'form':student})
