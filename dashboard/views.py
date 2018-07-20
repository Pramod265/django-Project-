from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from urllib.parse import urlparse
#from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from onboarding.models import DpyInstitute, DpyInstituteUsers, DpyUsers
from onboarding.serializers import InstituteUserSerializer, UserSerializer
from class_user_profiling.models import DpyInstituteUserClass,DpyInstituteClass,DpyInstituteAdditionalField,DpyInstituteUserAdditionalField
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.


def calculate_profile(request):
	profile_count = 0
	total_col = 35
	studentsArr = []
	teachersArr = []
	profileArr = [] 
	instituteArr = []
	# print(request.session['user_info'])
	queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
	serializer = InstituteUserSerializer(queryset)
	InstUserid = (serializer.data["id"])
	InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
	InstUserarr = ['role','designation','date_of_joining','is_active','status','institute_id','user_id']
	User = DpyUsers.objects.get(id=InstUser.user_id)
	Userarr = ['username','first_name','last_name','is_staff','is_active','date_joined','email','middle_name','mobile','dob','image','status' ]
	Institute = DpyInstitute.objects.get(id=InstUser.institute_id)
	
	if InstUser.role == None or InstUser.role == "":
		profile_count += 1

	if InstUser.designation == None or InstUser.designation == "":
		profile_count += 1

	if InstUser.date_of_joining == None or InstUser.date_of_joining == "":
		profile_count += 1

	if InstUser.status == None or InstUser.status == "":
		profile_count += 1

	if User.username == None or User.username == "":
		profile_count += 1

	if User.first_name == None or User.first_name == "":
		profile_count += 1

	if User.last_name == None or User.last_name == "":
		profile_count += 1

	if User.is_staff == None or User.is_staff == "":
		profile_count += 1

	
	if User.email == None or User.email == "":
		profile_count += 1

	if User.middle_name == None or User.middle_name == "":
		profile_count += 1

	if User.mobile == None or User.mobile == "":
		profile_count += 1

	if User.dob == None or User.dob == "":
		profile_count += 1

	if User.image == None or User.image == "":
		profile_count += 1

	if Institute.name == None or Institute.name == "":
		profile_count += 1


	if Institute.institute_email == None or Institute.institute_email == "":
		profile_count += 1


	if Institute.contact == None or Institute.contact == "":
		profile_count += 1


	if Institute.board == None or Institute.board == "":
		profile_count += 1


	if Institute.nature == None or Institute.nature == "":
		profile_count += 1

	if Institute.logo == None or Institute.logo == "":
		profile_count += 1

	if Institute.institute_image == None or Institute.institute_image == "":
		profile_count += 1

	if Institute.medium == None or Institute.medium == "":
		profile_count += 1

	if Institute.university == None or Institute.university == "":
		profile_count += 1

	if Institute.address == None or Institute.address == "":
		profile_count += 1

	if Institute.city == None or Institute.city == "":
		profile_count += 1

	if Institute.pin_code == None or Institute.pin_code == "":
		profile_count += 1

	if Institute.state == None or Institute.state == "":
		profile_count += 1

	if Institute.country == None or Institute.country == "":
		profile_count += 1

	studentIds=[]
	Inst_users = DpyInstituteUsers.objects.all().filter( institute_id=InstUser.institute_id,role=7,type=1)
	for inst_user in Inst_users:
		studentIds.append(inst_user.user_id)
	students = DpyUsers.objects.all().filter(id__in=studentIds)
	print("length of dpyuser",len(students))
	incomplete_students = [] #will take this array's length for total incomolete students detail in one institute
	# counter = 0
	for student in students:
		print(student.first_name)
		if student.first_name == "" or student.middle_name == "" or student.last_name == "" or student.mother_name == "" or student.date_joined == "" or student.email == "" or student.mobile == "" or student.dob == "" or student.gender == "" or student.blood_group == "" or student.caste == "" or student.nationality == "" or student.address == "" or student.address2 == "" or student.caste == "" or student.place_of_birth == "" or student.nationality == "" or student.first_name == None or student.middle_name == None or student.last_name == None or student.mother_name == None or student.date_joined == None or student.email == None or student.mobile == None or student.dob == None or student.gender == None or student.blood_group == None or student.caste == None or student.nationality == None or student.address == None or student.address2 == None or student.caste == None or student.place_of_birth == None or student.nationality == None:
			incomplete_students.append(student.id)
		
	percentage = ((27+1)-(profile_count+len(incomplete_students)))/27 * 100

	print(User.first_name)
	print("length of incompleteuser",len(incomplete_students))
	return int(percentage), incomplete_students



@login_required(login_url='/')
def home_view(request):
	if request.user.is_authenticated:
		colleges = DpyInstitute.objects.all()
		count,incomplete_students = calculate_profile(request)
		# print(incomplete_students)
		incomplete_student_no = len(incomplete_students)
		previous_url = request.META.get('HTTP_REFERER')
		print(urlparse(previous_url).path)
		if urlparse(previous_url).path == '/dashboard/home/':
			return render(request,'dashboard/home.html',{'institutes':colleges,'count':count, 'incomplete_students':incomplete_student_no})    #'deactivated_account':1
		return render(request,'dashboard/home.html',{'institutes':colleges,'count':count, 'incomplete_students':incomplete_student_no})
	return redirect('login_view')


@login_required(login_url='/')
def profile_view(request):
    if request.user.is_authenticated:
        return render(request,'dashboard/profile.html',{})
    return redirect('login_view')

@login_required(login_url='/')
def profile_edit(request):
    if request.user.is_authenticated:
        return render(request,'dashboard/profile_edit.html',{})
    return redirect('login_view')

class ManageProfile(APIView):
    permission_classes = (IsAuthenticated,)

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

# bulk upload view
import logging
import csv, io, html, string
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
# from .forms import Students_reg_form
# from .resources import StudentsResource, UsersResource
from tablib import Dataset
import json


@login_required(login_url='/')



def view_students(request):
	if request.method == 'GET':
		queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
		serializer = InstituteUserSerializer(queryset)
		institute_id = (serializer.data["user_id"])

		InstUser = DpyInstituteUsers.objects.all().filter(institute_id=request.session['institute_id'],role=7,type=1)
		UserStudentIds = []
		#this for loop is to take ids of all the studentds from user table
		for user in InstUser:
			if user.type == 1:
				UserStudentIds.append(user.user_id)

		students = DpyUsers.objects.all().filter(id__in = UserStudentIds,status=1)
		Institute_users_class = DpyInstituteUserClass.objects.all().filter(user_id__in=UserStudentIds,user_type=1)
	 
		classIds = []
		for user_class in Institute_users_class:
			classIds.append(user_class.ic_id)
		institute_class = DpyInstituteClass.objects.all().filter(id__in=classIds)
		return render(request,"dashboard/view_student.html",{'students':students,'Institute_users_class':Institute_users_class,'institute_class':institute_class})



def student_profile(request, id=None):
	instUser = DpyInstituteUsers.objects.get(user_id=id)
	student = DpyUsers.objects.get(id=id)
	Institute_users_class = DpyInstituteUserClass.objects.all().filter(user_id=id,user_type=1)
	if len(Institute_users_class) >= 1:
		institute_class = DpyInstituteClass.objects.get(id = Institute_users_class[0].ic_id)
	else:
		institute_class = {'standard':"NA",'division':'NA'}
	
	all_classes= DpyInstituteClass.objects.all().filter(institute_id=instUser.institute_id)
	print('roll no '+ Institute_users_class[0].roll_no)
	AdditionFields = DpyInstituteAdditionalField.objects.all().filter(institute_id = instUser.institute_id)
	UserAdditionalFields = DpyInstituteUserAdditionalField.objects.all().filter(user_id=id)
	all_students = DpyUsers.objects.all()
	return render(request,'dashboard/student_profile.html',{'form':student,'Institute_users_class':Institute_users_class,'institute_class':institute_class,'AdditionFields':AdditionFields,
		'UserAdditionalFields':UserAdditionalFields,'all_classes':all_classes,
		'all_students':all_students})
	return HttpResponse("sfadf"+id)



@login_required(login_url='/')
def profile_edit(request):
	if request.user.is_authenticated:
		return render(request,'dashboard/profile_edit.html',{})
	return redirect('login_view')

@csrf_exempt
def update_profile(request):
	if request.method == 'POST':
		formData = request.POST.getlist('formData[]')
		for i in range(0,len(formData)):
			if formData[i]=="none" or formData[i]==" " :
				formData[i]=""
		
		DpyUsers.objects.filter(id=formData[0]).update(
		email=formData[1],
		mobile=formData[2],
		)
		DpyInstituteUsers.objects.filter(user_id=formData[0]).update(
		role=formData[3],
		)
		DpyInstitute.objects.filter(id=formData[4]).update(
		name=formData[5],
		contact=formData[6],
		address=formData[7],
		) 
		#return Response({"status": True, "message": "Updated Successfully."}, status=status.HTTP_201_UPDATED)
		response_data ={'Status':True, 'Message': formData[0] }
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	return render(request,'dashboard/profile.html',{})
	

def incomplete_student(request):
	count,incomplete_students = calculate_profile(request)
	for i in range(0,len(incomplete_students),1):
		print(incomplete_students[i])
	students = DpyUsers.objects.filter(id__in=incomplete_students)
	return render(request,'dashboard/incomplete_students.html',{'students':students})
	return HttpResponse('incomplete students')


@login_required(login_url='/')
def update_password(request):
	if request.user.is_authenticated:
		if request.method == 'GET':
			return render(request,'dashboard/update_password.html',{})
		# if request.method == 'POST':
		#     formData = request.POST.getlist('formData[]')
		#     print(formData[0])
		#     DpyUsers.objects.filter(id = formData[0]).update(password=formData[1])
		#     response_data ={'Status':True, 'Message':'done'}
		#     return HttpResponse(json.dumps(response_data), content_type="application/json") 
	return redirect('login_view')

@login_required(login_url='/')
def reset_profile(request):
	if request.user.is_authenticated:
		DpyUsers.objects.filter(id=request.user.id).update(is_active=0)
		return redirect('dashboard:home')
		# return render(request,'dashboard/home.html',{})

@csrf_exempt
def update_student_personal(request,id=None):
	if request.method == 'POST':
		userData = json.loads(request.POST.get('user'))
		image = None
		if request.FILES.get('image') is not None :
			image = request.FILES.get('image')
		else:
			forImageFile = DpyUsers.objects.get(id=id)
			image = forImageFile.image
			print(image)
		array = ['first_name','last_name','email','middle_name','mobile','dob','blood_group',
		'religion','caste','mother_name','nationality','place_of_birth',
		'address','address2.date_of_addmission','gender','blood_group']

		DpyUsers.objects.filter(id=id).update(first_name = userData['first_name'],
			middle_name = userData['middle_name'],last_name=userData['last_name'],mobile = userData['mobile'],
			email = userData['email'],dob = userData['dob'],
			blood_group = userData['blood_group'],religion = userData['religion'],
			caste = userData['caste'],mother_name = userData['mother_name'],
			nationality = userData['nationality'],place_of_birth = userData['place_of_birth'],
			address = userData['address'],address2 = userData['address2'],
			date_joined = userData['date_joined'],gender = userData['gender'],image=image)
		
		response_data ={'Status':True, 'Message': 'succesfully updated' }
		return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def update_student_other(request,id=None):
	if request.method == 'POST':
		classData = json.loads(request.POST.get('class_details'))
		additional_fields = json.loads(request.POST.get('additional_fields'))
		queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
		serializer = InstituteUserSerializer(queryset)
		InstUserid = (serializer.data["id"])
		InstUser = DpyInstituteUsers.objects.get(id=request.user.id)
		inst_class = DpyInstituteClass.objects.all().filter(institute_id = InstUser.institute_id)
		AdditionFields = DpyInstituteAdditionalField.objects.all().filter(institute_id = InstUser.institute_id)
		# print("roll_no="+classData['roll_no'] +"ic_id="+classData['student_class'])
		# user_class, created =  DpyInstituteUserClass.objects.get_or_create(user_id=id)
		# if created:
		# 	inst_user_class = DpyInstituteUserClass.objects.filter(user_id=id).update(roll_no=classData['roll_no'],ic_id=classData['student_class'])
		# 	# inst_user_class.save()
		# else:
		# 	DpyInstituteUserClass.objects.filter(user_id=id).update(roll_no=classData['roll_no'],ic_id=classData['student_class'])

		user_class, created = DpyInstituteUserClass.objects.update_or_create(user_id=id, defaults = {'roll_no':classData['roll_no'],'ic_id':classData['student_class'],})
		for field in AdditionFields:
			DpyInstituteUserAdditionalField.objects.filter(user_id=id,iaf_id=field.id).update(value = additional_fields[field.key_name],updated_by=request.user.id)

		response_data ={'Status':True, 'Message': 'succesfully updated' }
		return HttpResponse(json.dumps(response_data), content_type="application/json")

from .forms import FeedbackForm
def feedback(request):
	if request.method == 'POST':
		form = FeedbackForm(request.POST)
 
		if form.is_valid():
			form.save()
			return render(request, 'dashboard/thanks.html')
	else:
		form = FeedbackForm()
	return render(request, 'dashboard/feedback_form.html', {'form': form})