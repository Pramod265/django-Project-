from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from onboarding.models import DpyInstitute,DpyInstituteUsers,DpyUsers
# from dashboard.models import DpyStudents
from .models import DpyFeeType, DpyInstituteClassFee,DpyFeeTransaction,DpyPaymentReceipt,DpyUserFeeIgnore
from django.http import HttpResponse
import json
from class_user_profiling.models import DpyDepartment, DpyInstituteClass, DpyInstituteClassSession, DpyInstituteClassSessionSubject,DpyInstituteUserClass
from onboarding.serializers import InstituteUserSerializer, UserSerializer
# Create your views here.


from django.views.decorators.csrf import csrf_exempt
@login_required(login_url='/')
@csrf_exempt

def add_fee(request):
	queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
	serializer = InstituteUserSerializer(queryset)
	InstUserid = (serializer.data["id"])
	InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
	# students = DpyStudents.objects.all().filter(institute_id = InstUser.institute_id).order_by('student_class','section')
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
		class_section = one_class.division
		institute_classes.append(institute_class+""+class_section)
	if request.method == 'GET':
		return render(request,'fees_management/add_fee.html',{'section_class':institute_classes})


	if request.method == 'POST':
		formData = request.POST.getlist('formData[]')
		classes = request.POST.getlist('classes[]')
		# print(formData[0][0]);
		# for i in range(0,len(formData),1):
		print(formData);
		fee = DpyFeeType(desc=formData[0])
		fee.save()
		# for i in range(0,len(classes),1):
		# 	one_class = classes[i]
		# 	fee_class = one_class[:-1]
		# 	section = one_class[-1:]
		# 	print(fee_class)
		# 	print(section)

		for j in range(0,len(classes),1):
			one_class = classes[j]
			fee_class = one_class[:-1]
			section = one_class[-1:]
			print(fee_class)
			print(section)
			classes_id =  DpyInstituteClass.objects.all().filter(standard=fee_class,division=section,institute_id=InstUser.institute_id)
			for class_id in classes_id:
				print(class_id.id)
				this_class = class_id.id
			inst_class_fee = DpyInstituteClassFee(amount=int(formData[1]),display_name=formData[0],cycle=formData[2],bifurcations='-',fee_type_id=fee.id,institute_class_id=this_class)
			inst_class_fee.save()
		response_data ={'Status':True, 'Message': "succesfully added" }
		return HttpResponse(json.dumps(response_data), content_type="application/json")
		return render(request,'fees_management/add_fee.html',{})

@csrf_exempt
def fee_types(request):
	queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
	serializer = InstituteUserSerializer(queryset)
	InstUserid = (serializer.data["id"])
	InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
	# institute_id = InstUser.institute_id
	classes_ids = []
	total_classes = DpyInstituteClass.objects.all().filter(institute_id = InstUser.institute_id).order_by('standard','division')
	for one_class in total_classes:
		classes_ids.append(one_class.id)

	#now we are taking out all the fees from one instititute
	total_types_fees = DpyInstituteClassFee.objects.filter(institute_class_id__in=classes_ids)
	types_of_fees = DpyFeeType.objects.all()
	#here now we will fetch distinc types of fees from inst_class_fee
	matrix =[]
	class_array = []
	# for fee in types_of_fees:
	# 	for type_fee in total_types_fees:
	# 		if fee.id == type_fee.fee_type_id:
	# 			# class_to_add = DpyInstituteClass.objects.filter(id = type_fee.institute_class_id)
	# 			class_array.append(type_fee.institute_class_id)
	# 	matrix[0].append(class_array)

	# print(matrix)
	total_types_fees_ids = []
	# counter = 0
	# for type_fee in total_types_fees:
	# 	if counter >= 1:
	# 		if type_fee.fee_type_id in total_types_fees_ids:
	# 			continue
	# 	total_types_fees_ids.append(type_fee.fee_type_id)
	# 	counter += 1
	# print(total_types_fees_ids)
	# total_types_fees = DpyInstituteClassFee.objects.filter(fee_type_id__in=total_types_fees_ids,institute_class_id__in=classes_ids)
	# total_types_fees.exclude(fee_type_id=1)
	# print(total_types_fees[0].id)

	if request.method == 'GET':
		return render(request,"fees_management/fee_types.html",{'total_classes':total_classes,'total_types_fees':total_types_fees,'total_types_fees_ids':total_types_fees_ids,'types_of_fees':types_of_fees})

	if request.method == 'POST':
		formData = request.POST.getlist('formData[]')
		DpyFeeType.objects.filter(id=formData[0]).update(desc=formData[1])
		DpyInstituteClassFee.objects.filter(fee_type_id=formData[0]).update(display_name=formData[1],amount=formData[2])
		response_data ={'Status':True, 'Message': 'success' }
		return HttpResponse(json.dumps(response_data), content_type="application/json")


def pay(request):
	queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
	serializer = InstituteUserSerializer(queryset)
	InstUserid = (serializer.data["id"])
	InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
	user = DpyUsers.objects.get(id=InstUser.user_id)

	# students = DpyStudents.objects.all().filter(institute_id=InstUser.institute_id).order_by('student_class', 'section')
	total_classes = DpyInstituteClass.objects.all().filter(
		institute_id=InstUser.institute_id).order_by('standard', 'division')
	fees = DpyInstituteClassFee.objects.all()
	institute = DpyInstitute.objects.all().filter(id=InstUser.institute_id)
	i = 0
	data = {}
	for one_class in total_classes:
		data[i] = {
			'class_sec': one_class.standard+one_class.division,
			'class_id': str(one_class.id)
		}
		i = i+1
	institute_classes = []
	counter = 0
	for one_class in total_classes:
		institute_class = one_class.standard
		class_section = one_class.division
		calss_id = str(one_class.id)
		institute_classes.append(institute_class+""+class_section)
	
	institute_users=DpyInstituteUsers.objects.all().filter(institute_id=InstUser.institute_id,type=1,role=7)
	studentIds=[]
	for institute_user in institute_users:
		studentIds.append(institute_user.user_id)
		# print(institute_user.user_id)
	students = DpyUsers.objects.all().filter(id__in=studentIds)
	# students = DpyInstituteUserClass.all().filter(user_id=)
	user_classes = DpyInstituteUserClass.objects.all().filter(user_id__in=studentIds)
	if request.method == 'GET':
		return render(request, 'fees_management/pay.html', {'section_class': data, 'total_classes': total_classes, 'students': students, 'fees': fees, 'institute': institute,'user_classes':user_classes})

	if request.method == 'POST':
		data = request.POST.getlist('feeData[]')
		student = DpyUsers.objects.get(id=data[8])
		fee = DpyFeeTransaction(dsc=data[0]+"-"+data[7], paid_amount=data[1], cycle=data[2], cycle_slot=int(data[3]),institute_class_fee_id=int(data[4]), status=1, mop=int(data[5]), receipt_id=int(data[6]), user=student)
		fee.save()

		response_data = {'Status': True, 'Message': 'Successfull'}
		return HttpResponse(json.dumps(response_data), content_type="application/json")
		return render(request, 'fees_management/pay.html', {})


def reciept(request):
	inst_id = institute_id(request)
	data = request.POST.getlist('data[]')
	u = DpyPaymentReceipt(mop=data[1],token_or_chequeno=data[2],receipt_amount=float(data[0]), status=1, institute_id_id=inst_id)
	u.save()
	rid = u.id
	response_data = {'Status': True,
					 'Message': 'Successfully Updated.', 'id': rid}
	return HttpResponse(json.dumps(response_data), content_type="application/json")

def transaction(request):
	inst_id = institute_id(request)
	data = request.POST.get('data')
	trans = DpyFeeTransaction.objects.all().filter(user_id=data)
	result_list = list(trans.values('institute_class_fee','cycle','paid_amount','dsc','cycle_slot'))
	return HttpResponse(json.dumps(result_list))

def updatetrans(request):
	inst_id = institute_id(request)
	# data.push(feename, feeamount, feecycyle, feecycleslot, feeid, mop, rid, feecyclename, student_id);
	data = request.POST.getlist('feeData[]')
	v = DpyFeeTransaction.objects.get(user_id=data[8],institute_class_fee=data[4],cycle=data[2],cycle_slot=data[3])
	amount = int(v.paid_amount)
	DpyFeeTransaction.objects.all().filter(user_id=data[8],institute_class_fee=data[4],cycle=data[2],cycle_slot=data[3]).update(paid_amount=amount+int(data[1]))
	response_data = {'Status': True,
					 'Message': 'Successfully Updated.'}
	return HttpResponse(json.dumps(response_data), content_type="application/json")

def institute_id(request):
	queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
	serializer = InstituteUserSerializer(queryset)
	institute = serializer.data['institute']
	inst_id = institute['id']
	return inst_id

def getclass(request):
	data = request.POST.get('data')
	user_classes = DpyInstituteUserClass.objects.all().filter(user_id=data)
	for i in user_classes:
		uid= i.ic_id
		print(i.ic_id)
	classsec = DpyInstituteClass.objects.all().filter(id=uid)
	for j in classsec:
		standard= j.standard
		division= j.division
	response_data = {'Status': True,'Message': 'Successfully Updated.', 'cs':standard+""+division}
	return HttpResponse(json.dumps(response_data), content_type="application/json")