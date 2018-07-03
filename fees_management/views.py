from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
# from urllib.parse import urlparse
# from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from onboarding.models import DpyInstitute, DpyInstituteUsers, DpyUsers
from dashboard.models import DpyStudents
from .models import DpyFeeType, DpyInstituteClassFee
from class_user_profiling.models import DpyDepartment, DpyInstituteClass, DpyInstituteClassSession, DpyInstituteClassSessionSubjects 
from onboarding.serializers import InstituteUserSerializer, UserSerializer
# Create your views here.

def add_fee(request):
	queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
	serializer = InstituteUserSerializer(queryset)
	InstUserid = (serializer.data["id"])
	InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
	students = DpyStudents.objects.all().filter(institute_id = InstUser.institute_id).order_by('student_class','section')
	total_classes = DpyInstituteClass.objects.all().filter(institute_id = InstUser.institute_id).order_by('standard','division')
	# section_class = []
	institute_classes = []
	counter = 0
	# for student in students:
	# 	student_class = student.student_class
	# 	student_section =student.section
	# 	student_class_section = student_class +" "+ student_section
	# 	if student_class_section in section_class:
	# 		continue
	# 	print(student_class_section)
	# 	section_class.append(student_class_section)
	for one_class in total_classes:
		institute_class = one_class.standard
		institute_classes.append(institute_class)
	if request.method == 'GET':
		return render(request,'fees_management/add_fee.html',{'section_class':institute_classes,'students':students})
	# return render(request,'add_fee.html',{})

	if request.method == 'POST':
		formData = request.POST.getlist('formData[]')
		classes = request.POST.getlist('classes[]')
		fee = DpyFeeType.objects.save(desc=formData[0])
		InstituteClass = DpyInstituteClass.objects.get(institute_id=serializer.data["institute"])
		for one_class in classes:
			fee_class = one_class[:-2]
			section = one_class[-1:]
			print(student_class)
			print(section)
			fee_class_section = DpyInstituteClass 
			DpyInstituteClassFee.objects.save(desc=formData[0],)

		return render(request,'fees_management/add_fee.html',{})