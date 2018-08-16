from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from onboarding.models import DpyInstitute, DpyInstituteUsers, DpyUsers,DpyUpdateLog
# from dashboard.models import DpyStudents
from .models import DpyInstituteClassFee, DpyFeeTransaction, DpyPaymentReceipt, DpyUserFeeIgnore
from django.http import HttpResponse
import json
from .serializers import DpyInstituteClassFeeSerializer, DpyUserFeeIgnoreSerializer,DpyFeeTransactionSerializer,DpyPaymentReceiptSerializer
from rest_framework.viewsets import ModelViewSet
from class_user_profiling.models import DpyDepartment, DpyInstituteClass, DpyInstituteClassSession, DpyInstituteClassSessionSubject, DpyInstituteUserClass
from onboarding.serializers import InstituteUserSerializer, UserSerializer
# Create your views here.
from class_user_profiling.serializers import DpyInstituteClassSerializer

from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/')
@csrf_exempt
# def add_fee(request):
# 	queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
# 	serializer = InstituteUserSerializer(queryset)
# 	InstUserid = (serializer.data["id"])
# 	InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
# 	# students = DpyStudents.objects.all().filter(institute_id = InstUser.institute_id).order_by('student_class','section')
# 	total_classes = DpyInstituteClass.objects.all().filter(institute_id = InstUser.institute_id).order_by('standard','division')
# 	# section_class = []
# 	institute_classes = []
# 	counter = 0
# 	for one_class in total_classes:
# 		institute_class = one_class.standard
# 		class_section = one_class.division
# 		institute_classes.append(institute_class+""+class_section)
# 	if request.method == 'GET':
# 		classes  = DpyInstituteClassSerializer.get_classes(request)
# 		return render(request,'fees_management/add_fee.html',{'section_class':classes})
# 	if request.method == 'POST':
# 		formData = request.POST.getlist('formData[]')
# 		classes = request.POST.getlist('classes[]')
# 		print(formData);
# 		fee = DpyFeeType(desc=formData[0])
# 		fee.save()
# 		for j in range(0,len(classes),1):
# 			one_class = classes[j]
# 			fee_class = one_class[:-1]
# 			section = one_class[-1:]
# 			print(fee_class)
# 			print(section)
# 			classes_id =  DpyInstituteClass.objects.all().filter(standard=fee_class,division=section,institute_id=InstUser.institute_id)
# 			for class_id in classes_id:
# 				print(class_id.id)
# 				this_class = class_id.id
# 			inst_class_fee = DpyInstituteClassFee(amount=int(formData[1]),display_name=formData[0],cycle=formData[2],bifurcations='-',fee_type_id=fee.id,institute_class_id=this_class)
# 			inst_class_fee.save()
# 		response_data ={'Status':True, 'Message': "succesfully added" }
# 		return HttpResponse(json.dumps(response_data), content_type="application/json")
# 		return render(request,'fees_management/add_fee.html',{})
def fee_types(request):
	# queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
	# serializer = InstituteUserSerializer(queryset)
	# InstUserid = (serializer.data["id"])
	# InstUser = DpyInstituteUsers.objects.get(id=InstUserid)
	# # institute_id = InstUser.institute_id
	# classes_ids = []
	# total_classes = DpyInstituteClass.objects.all().filter(institute_id = InstUser.institute_id).order_by('standard','division')
	# for one_class in total_classes:
	# 	classes_ids.append(one_class.id)

	# #now we are taking out all the fees from one instititute
	# total_types_fees = DpyInstituteClassFee.objects.filter(institute_class_id__in=classes_ids)
	# # types_of_fees = DpyFeeType.objects.all()
	# #here now we will fetch distinc types of fees from inst_class_fee
	# matrix =[]
	# class_array = []
	# total_types_fees_ids = []

	# if request.method == 'GET':
	# 	return render(request,"fees_management/fee_types.html",{'total_classes':total_classes,'total_types_fees':total_types_fees,'total_types_fees_ids':total_types_fees_ids,'types_of_fees':types_of_fees})

	# if request.method == 'POST':
	# 	formData = request.POST.getlist('formData[]')
	# 	# DpyFeeType.objects.filter(id=formData[0]).update(desc=formData[1])
	# 	DpyInstituteClassFee.objects.filter(fee_type_id=formData[0]).update(display_name=formData[1],amount=formData[2])
	# response_data ={'Status':True, 'Message': 'success' }
	# return HttpResponse(json.dumps(response_data), content_type="application/json")
	return render(request, "fees_management/fee_types.html")


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

	institute_users = DpyInstituteUsers.objects.all().filter(
		institute_id=InstUser.institute_id, type=1, role=7)
	studentIds = []
	for institute_user in institute_users:
		studentIds.append(institute_user.user_id)
		# print(institute_user.user_id)
	students = DpyUsers.objects.all().filter(id__in=studentIds)
	# students = DpyInstituteUserClass.all().filter(user_id=)
	user_classes = DpyInstituteUserClass.objects.all().filter(user_id__in=studentIds)
	if request.method == 'GET':
		return render(request, 'fees_management/pay.html', {'section_class': data, 'total_classes': total_classes, 'students': students, 'fees': fees, 'institute': institute, 'user_classes': user_classes})

	if request.method == 'POST':
		data = request.POST.getlist('feeData[]')
		student = DpyUsers.objects.get(id=data[8])
		u = DpyFeeTransaction.objects.all().filter(dsc=data[0]+"-"+data[7], paid_amount=data[1], cycle=data[2], cycle_slot=int(
			data[3]), institute_class_fee_id=int(data[4]), status=1, mop=int(data[5]), user=student)
		# print("u"+u.count())
		if u.count() >= 1:
			response_data = {'Status': False,
							 'Message': "Fee Transaction Already exists"}
		else:
			fee = DpyFeeTransaction(dsc=data[0]+"-"+data[7], paid_amount=data[1], cycle=data[2], cycle_slot=int(
				data[3]), institute_class_fee_id=int(data[4]), status=1, mop=int(data[5]), receipt_id=int(data[6]), user=student)
			fee.save()
			response_data = {'Status': True, 'Message': "Success!!"}

		return HttpResponse(json.dumps(response_data), content_type="application/json")
		return render(request, 'fees_management/pay.html', {})


def reciept(request):
	inst_id = institute_id(request)
	data = request.POST.getlist('data[]')
	u = DpyPaymentReceipt(mop=data[1], token_or_chequeno=data[2], receipt_amount=float(
		data[0]), status=1, institute_id_id=inst_id)
	u.save()
	rid = u.id
	response_data = {'Status': True,
					 'Message': 'Successfully Updated.', 'id': rid}
	return HttpResponse(json.dumps(response_data), content_type="application/json")


def transaction(request):
	inst_id = institute_id(request)
	data = request.POST.get('data')
	trans = DpyFeeTransaction.objects.all().filter(user_id=data)
	result_list = list(trans.values('institute_class_fee',
									'cycle', 'paid_amount', 'dsc', 'cycle_slot'))
	return HttpResponse(json.dumps(result_list))


def updatetrans(request):
	inst_id = institute_id(request)
	# data.push(feename, feeamount, feecycyle, feecycleslot, feeid, mop, rid, feecyclename, student_id);
	data = request.POST.getlist('feeData[]')
	v = DpyFeeTransaction.objects.get(
		user_id=data[8], institute_class_fee=data[4], cycle=data[2], cycle_slot=data[3])
	amount = int(v.paid_amount)
	DpyFeeTransaction.objects.all().filter(
		user_id=data[8], institute_class_fee=data[4], cycle=data[2], cycle_slot=data[3]).update(paid_amount=amount+int(data[1]))
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
		uid = i.ic_id
		print(i.ic_id)
	classSec = DpyInstituteClass.objects.all().filter(id=uid)
	for j in classSec:
		standard = j.standard
		division = j.division
	response_data = {
		'Status': True, 'Message': 'Successfully Updated.', 'cs': standard+""+division}
	return HttpResponse(json.dumps(response_data), content_type="application/json")


"""
###############################################
API FOR MANAGEMENT OF FEES add , get AND update
###############################################
"""


def update_log(request,table_name,table_id,previousVal,newVal):
	'''
	################################################################
	This function is used to store data in update_log
	@param previousVal is the dictionary value of data before update
	@param newVal is the dictionary of particular data to be updated
	################################################################ 
	'''
	previous_data = {}
	update_data = {}
	final_data = {}
	for key,value in newVal.items():
		
		# print(str(key) +":--"+ str(value))
		keys = key
		print(keys)

		update_data[key]=value
		previous_data[key]=previousVal.data[keys]

	# final_data.setdefault('update_log', {'new':update_data}).setdefault('previous',{}).update(previous_data)
	final_data['new_val'] = update_data
	final_data['old_val'] = previous_data

	DpyUpdateLog.objects.create(table_name=table_name,
		table_id=table_id,desc=final_data,added_by=request.user.id)


class Fees(ModelViewSet):
	serializer_class = DpyInstituteClassFeeSerializer
	queryset = DpyInstituteClassFee.objects.all()

	def get_fees(self, request):
		'''
		###############################################
		FUNCTION TO RETURN FEES IN THE FORM OF JSON obj
		###############################################
		'''
		instid = request.GET.get('id')
		classes = DpyInstituteClass.objects.all().filter(institute_id=instid)
		fees_in_class = {}
		final_data = {}

		# ------------CHEKING IF WE ARE RECEIVING ANY ARRAY OF SELECTED CLASS ids
		if request.GET.getlist('inst_classes[]'):
			ids = request.GET.getlist('inst_classes[]')
			q1 = DpyInstituteClassFee.objects.all().filter(institute_class__in=ids, status=1)
			fees_in_class = DpyInstituteClassFeeSerializer(q1, many=True)

			# -----------HERE CREATING JSON OBJ TO THE GIVEN CLASSES ids
			for value in fees_in_class.data:
				final_data.setdefault(
					value['institute_class'], []).append(value)
				# print(value)
			return Response({"status": True, "message": "Fee Detail For Selected Class.", "data": final_data})
		else:  # -------SINCE WE DID NOT RECIEVED ANY CLASS id ARRAY THEREFORE RETURNG ALL THE FEES

			# -------------THIS FOR IS FOR TAKING ids OF ALL THE CLASSES IN THE INSTITUTE
			class_ids = []
			for one_class in classes:
				class_ids.append(one_class.id)

			print(class_ids)
			q1 = DpyInstituteClassFee.objects.all().filter(
				institute_class_id__in=class_ids, status=1)
			fees_in_class = DpyInstituteClassFeeSerializer(q1, many=True)
			hierarchy = "Class_id ->classs_details{''},fees_id{'fees Details'}"

			# ----------HERE CREATING JSON OBJ TO ALL THE FEES ids
			for value in fees_in_class.data:
				obj = DpyInstituteClass.objects.get(
					id=value['institute_class'])
				final_data.setdefault(value['institute_class'], {'class_details': {
									  'sort_index': obj.sort_index, 'standard': obj.standard, 'division': obj.division}}).setdefault(value['id'], {}).update(value)
				# final_data[obj.standard+""+str(obj.division)].update({})
				# print(value['display_name']+"standard:"+str(obj.standard)+",division:"+str(obj.division)+"))")
			return Response({"status": True, "message": "Fee detail for all classes."+hierarchy, "data": final_data})

		return Response({"status": True, "message": "Class fees Data.", "data": fees_in_class})

	def new_fee(self, request):
		'''
		############################################################
		THIS FUNCTIONS CREATES NEW fees AND  IT WILL REQUIRE AN JSON 
		ARRAY obj FROM FRONTEND WHOSE FORMAT IS WRITTEN ON DEMO.JSON 
		############################################################
		'''
		formData = request.data
		print(formData);
		json_obj = json.dumps(formData)
		err = []
		success = []

		# ------------THIS FOR LOOP FETCH EVERY ELEMENT OF ARRAY OF 'fees' OBJ
		for data in formData:
			try:
				inst_class_fee = DpyInstituteClassFee(amount=int(data['amount']), display_name=data['display_name'], cycle=data['cycle'],
													  bifurcations=data['bifurcations'], institute_class_id=data['institute_class'], added_by=request.user.id)
				inst_class_fee.save()

				# -------------HERE APPENDING success obj WITH SUCCESS MESSAGE
				success.append(str(
					data['display_name']) + " Fees added for class " + str(data['institute_class']) + ".")
				# success = str(data['display_name']) + " Fees added for class " + str(data['institute_class']) + "."
			except Exception as e:
				# -------------HERE APPENDING err obj ERROR MESSAGE
				err.append(str(
					data['display_name']) + " Fees Already Exist for class " + str(data['institute_class']) + ".")
		return Response({"status": True, "message": "Class fees Added.", "data": {'success': success, 'error': err}})

	def partial_update(self, request):
		'''
		###################################################################
		THIS FUNCTION WILL UPDATE fees DATA,HERE IT WILL REQUIRE JSON ARRAY
		###################################################################
		'''
		formData = request.data
		json_obj = json.dumps(data)
		err = []
		success = []
		previousVal = ""
		final_data = {}

		# -------------THIS FOR LOOP FETCH EVERY ELEMENT OF ARRAY OF 'fees' OBJ
		for fee_data in formData.data:
			inst_class = DpyInstituteClass.objects.get(id=fee_data['institute_class'])
		# serialized = DpyInstituteClassFeeSerializer(data['id'],request.data,partial=True)

			try:
				q0 = DpyInstituteClassFee.objects.get(id=fee_data['id'])
				fees2 = DpyInstituteClassFeeSerializer(q0)
				
				# -----------PERFORMING ACTUALL UPDATE HERE

				serialized = DpyInstituteClassFee.objects.filter(id=fee_data['id']).update(**fee_data,updated_by=request.user.id)

				# -----------CREATING OBJECT OF FEES FOR STATUS MESSAGE
				q1 = DpyInstituteClassFee.objects.get(id=fee_data['id'])
				fees = DpyInstituteClassFeeSerializer(q1)
				# keys = "bifurcations"
				# print("fees.data['dispplay_name']"+fees.data['display_name'])

				# storing the values of fields after update
				# previous_data = {}
				# update_data = {}
				# array = []

				# for key,value in fee_data.items():

				# 	# print(str(key) +":--"+ str(value))he render function with parenthesis.
				# 	keys = key
				# 	print(keys)

				# 	update_data[key]=value
				# 	previous_data[key]=fees2.data[keys]

				# # final_data.setdefault('update_log', {'new':update_data}).setdefault('previous',{}).update(previous_data)
				# final_data['new_val'] = update_data
				# final_data['old_val'] = previous_data

				success.append("fees type "+str(fees.data['display_name'])+" updated for class "+str(
					inst_class.standard)+""+str(inst_class.division)+".")

				# ------------CALLING FUNCTION TO UPDATE LOG DATA
				update_log(request, 'DpyInstituteClassFee',
						   fee_data['id'], fees2, fee_data)

			except Exception as e:
				err.append(str(fees.data['display_name'])+" fees already exist for class " + str(
					inst_class.standard)+""+str(inst_class.division)+".")

		return Response({"status": True, "message": "Connection successful.", "data": {'success': success, 'error': err}})


def update_log(request, table_name, table_id, previousVal, newVal):
	'''
	################################################################
	This function is used to store data in update_log
	@param previousVal is the dictionary value of data before update
	@param newVal is the dictionary of particular data to be updated
	################################################################ 
	'''
	previous_data = {}
	update_data = {}
	final_data = {}
	for key, value in newVal.items():

		# print(str(key) +":--"+ str(value))
		keys = key
		print(keys)

		update_data[key] = value
		previous_data[key] = previousVal.data[keys]

	# final_data.setdefault('update_log', {'new':update_data}).setdefault('previous',{}).update(previous_data)
	final_data['new_val'] = update_data
	final_data['old_val'] = previous_data

	DpyUpdateLog.objects.create(table_name=table_name,
								table_id=table_id, desc=final_data, added_by=request.user.id)


class Fees_ignore(ModelViewSet):
	serializer_class = DpyInstituteClassFeeSerializer
	queryset = DpyInstituteClassFee.objects.all()

	def get_fees_ignore(self, request):
		'''
		#############################################################
		THIS FUNCTION WILL RETURN DATA OF fees TO IGNORE IN JSON FORM
		#############################################################
		'''
		instid = request.GET.get('id')
		all_students = DpyInstituteUsers.objects.all().filter(institute_id=instid,role=7,status=1)
		final_data = {}

		#------------CHEKING IF WE ARE RECEIVING ANY ARRAY OF SELECTED Students ids
		if request.GET.getlist('students[]'):
			
			ids = request.GET.getlist('students[]')
	
			q1 = DpyUserFeeIgnore.objects.all().filter(user_id__in=ids)
			users_fee_ignore = DpyUserFeeIgnoreSerializer(q1,many=True)
			
			# print(receipts_in_class)
			
			for value in users_fee_ignore.data:
				final_data.setdefault(value['user'],{}).setdefault(value['institute_class_fee'],{}).update(value)

			return Response({"status": True, "message": "User Fees Ignore Data.", "data": final_data})	

		else: #-------SINCE WE DID NOT RECIEVED ANY RECEIPT id ARRAY THEREFORE RETURNG ALL THE FEES

			student_ids = []
			for one_student in all_students:
				student_ids.append(one_student.user_id)

			q1 = DpyUserFeeIgnore.objects.all().filter(user_id__in=student_ids)
			users_fee_ignore = DpyUserFeeIgnoreSerializer(q1,many=True)
			
			# print(receipts_in_class)
			
			for value in users_fee_ignore.data:
				final_data.setdefault(value['user'],{}).setdefault(value['institute_class_fee'],{}).update(value)

			return Response({"status": True, "message": "User Fees Ignore Data.", "data": final_data})	



	def new_fees_ignore(self, request):
		'''
		########################################################
		THIS FUNCTION IS GOING TO ADD NEW fee_ignore TO STUDENTS. 
		IF IT'S ALREADY EXIST IT WILL UPDATE THE DATA.
		########################################################
		'''
		formData = request.data
		# print(formData);
		json_obj = json.dumps(formData)
		err = []
		success = []
		final_data = {}
		# -------------THIS for LOOP FETCH EVERY OBJ OF USER id
		for k, v in formData.items():

			classUser = DpyUsers.objects.get(id=k)

			# -----------THIS for LOOP IS FOR EVERY FEES OBJECT id IN ONE STUDENT'S OBJECT
			for k1, v1 in v.items():

				classFee = DpyInstituteClassFee.objects.get(id=k1)

				try:
					print("value1" + str(v1))

					# -----------------CHECKING IF PARTICULAR FEES EXIST OR NOT IF IT'S EXIST THEN UPDATE
					if classFee.status == 1:

						if int(v1['percent_discount']) > 100:
    							err.append(str(
								classFee.display_name)+" Fees discount percentage can not be greater than 100 .")
						else:

							inst_user_fee_ignore = DpyUserFeeIgnore(
								percent_discount=v1['percent_discount'], status=v1['status'], user_id=k, institute_class_fee_id=k1, added_by=request.user.id)
							inst_user_fee_ignore.save()

							# ----------------HERE APPENDING SUCCESS obj WITH SUCCESS MESSAGE
							success.append(str(classFee.display_name) + " Fees discount of " + str(
								v1['percent_discount']) + "percent has been allocated for user " + str(classUser.first_name))

					else:
						err.append(str(classFee.display_name) +
								   " Fees has been disabled by your admin.")

				except Exception as e:

					q1 = DpyUserFeeIgnore.objects.get(
						user_id=k, institute_class_fee_id=k1)
					fees_ignore = DpyUserFeeIgnoreSerializer(q1)

					# --------------UPDATING THE fees_ignore FOR USER IF IT'S ALREADY EXIST
					DpyUserFeeIgnore.objects.filter(user_id=k, institute_class_fee_id=k1).update(**v1, updated_by=request.user.id)

					update_log(request, 'DpyUserFeeIgnore',
							   q1.id, fees_ignore, value1)

					success.append(str(classFee.display_name) + " Fees discount of " +
								   str(v1['percent_discount']) +
								   "percent has been updated for user " + str(classUser.first_name))

		return Response({"status": True, "message": "Successfull.", "data": {'success': success, 'error': err}})


class Fees_pay(ModelViewSet):
	
	serializer_class = DpyFeeTransactionSerializer
	queryset = DpyFeeTransaction.objects.all()

	def get_fees_pay(self,request):
		'''
		#########################################################################
		THIS METHOD WILL RETURN DATA OF RECEIPT INCLUDING DATA OF ALL THE TRANSACTIONS
		IN THAT RECEIPT
		#########################################################################
		'''
		student_ids = []
		final_data = {}
		users = DpyInstituteUsers.objects.all().filter(institute_id=request.GET.get('id'))
		for user in users:
			student_ids.append(user.user_id)
		Students = DpyUsers.objects.all().filter(id__in=student_ids)
		#------------CHEKING IF WE ARE RECEIVING ANY ARRAY OF SELECTED RECEIPTS ids
		if request.GET.getlist('students_arr[]'):
			ids = request.GET.getlist('students_arr[]')

			q1 = DpyFeeTransaction.objects.all().filter(user_id__in=ids)
			transactions_in_receipt = DpyFeeTransactionSerializer(q1,many=True)

			for value in transactions_in_receipt.data:
				qset = DpyUserFeeIgnore.objects.all().filter(user_id=value['user_id'])
				final_data.setdefault(value['user_id'],{}).setdefault('transactions',{}).setdefault(value['id'],{}).update(value)
				# for fee_ignore in qset:
				# 	final_data.setdefault(value['user_id'],{}).setdefault('fee_ignore',{}).setdefault(str(fee_ignore.institute_class_fee_id),{}).update({'percent_discount':str(fee_ignore.percent_discount),
				# 	'status':str(fee_ignore.status),'institute_class_fee_id':str(fee_ignore.institute_class_fee_id)})
			

			#---------------CHECKING IF USER HAS ANY FEES PAID OR NOT
			# if len(q1) == 0:
			Students = DpyUsers.objects.all().filter(id__in=ids)
			for student in Students:
				qset = DpyUserFeeIgnore.objects.all().filter(user_id=student.id)
				final_data.setdefault(student.id,{}).setdefault('transactions',{})
				for fee_ignore in qset:
					final_data.setdefault(student.id,{}).setdefault('fee_ignore',{}).setdefault(str(fee_ignore.institute_class_fee_id),{}).update({'percent_discount':str(fee_ignore.percent_discount),
					'status':str(fee_ignore.status),'institute_class_fee_id':str(fee_ignore.institute_class_fee_id)})

			return Response({"status": True, "message": "Fees Receipt Data.", "data": final_data})	

		else: #------------SINCE WE DID NOT RECIEVED ANY RECEIPT id ARRAY THEREFORE RETURNG ALL THE FEES

			student_ids = []
			for one_student in Students:
				student_ids.append(one_student.id)

			q1 = DpyFeeTransaction.objects.all().filter(user_id__in=student_ids)
			
			transactions_in_receipt = DpyFeeTransactionSerializer(q1,many=True)

			for value in transactions_in_receipt.data:
				qset = DpyUserFeeIgnore.objects.all().filter(user_id=value['user_id'])
				# fee_ignore = DpyUserFeeIgnoreSerializer(qset)
				final_data.setdefault(value['user_id'],{}).setdefault('transactions',{}).setdefault(value['id'],{}).update(value)
				# for fee_ignore in qset:
				# 	final_data.setdefault(value['user_id'],{}).setdefault('fee_ignore',{}).setdefault(str(fee_ignore.institute_class_fee_id),{}).update({'percent_discount':str(fee_ignore.percent_discount),
				# 	'status':str(fee_ignore.status),'institute_class_fee_id':str(fee_ignore.institute_class_fee_id)})

			#---------------CHECKING IF USER HAS ANY FEES PAID OR NOT
			# if len(q1) == 0:
			Students = DpyUsers.objects.all().filter(id__in=student_ids)
			for student in Students:
				qset = DpyUserFeeIgnore.objects.all().filter(user_id=student.id)
				final_data.setdefault(student.id,{}).setdefault('transactions',{})
				for fee_ignore in qset:
					final_data.setdefault(student.id,{}).setdefault('fee_ignore',{}).setdefault(str(fee_ignore.institute_class_fee_id),{}).update({'percent_discount':str(fee_ignore.percent_discount),
					'status':str(fee_ignore.status),'institute_class_fee_id':str(fee_ignore.institute_class_fee_id)})


			return Response({"status": True, "message": "ALL Fees Receipt Data.", "data": final_data})	


	def new_fees_pay(self,request):
		'''
		############################################################
		THIS METHOD CREATES RECORD FOR TRANSACTIONS AND ON THE B BASIS OF
		TRANSACTIONS IT CREATES FEE RECEIPT
		@param json - POST('userId':=>'icf_id':{'paid_amount','mop','cycle_slot'})
		############################################################
		'''
		success = []
		err = []
		instid = request.GET.get('id')
		data = request.data
		paymet_receipt_id = ''
		receipt_amount = 0
		status = 0
		mop = 0
		chequeNo = None
		#-----------THIS for LOOP IS FOR EVERY FEES OBJECT id IN ONE STUDENT'S OBJECT 
		for k2,v2 in data.items():

			classUser = DpyUsers.objects.get(id=k2)

			#------------THIS loop JOB IS TO add PAID AMOUNT OF ALL TRANSACTIONS
			for k3,v3 in v2.items():
				for k4,v4 in v3.items():
					classFee = DpyInstituteClassFee.objects.get(id=k3)

					any_transaction = DpyFeeTransaction.objects.all().filter(cycle_slot=k4,
						user_id=k2,institute_class_fee_id=k3)

					fees_ignore = DpyUserFeeIgnore.objects.all().filter(user_id=k2,institute_class_fee_id=k3)
					print('v4' + str(v4))
					for k5,v5 in v4.items():
						print('v5'+str(v5))
						#----------CHECKING IF USER GOT ANY PREVIOUS TRANSACTION DONE FOR PARTICULAR FEES CYCLE
						if len(any_transaction) > 0:
							remaining_fee = classFee.amount - int(any_transaction[0].paid_amount)
							#------------IF USER HAS ALREADY PAID THEN CHECKING REMAINING FEES TO BE PAID
							if remaining_fee < int(v5['paid_amount']):
								err.append('Error. You have already paid Rs. '+ str(any_transaction[0].paid_amount) + ' for fees '+str(classFee.display_name)+' this time you tried to pay more than remaing.It\'s not get added in receipt.')
								continue

						#----------CHECKING IF USER GOT ANY DISCOUNT ON PARTICULAR FEES OR NOT
						if len(fees_ignore) > 0:
							percent_discount = fees_ignore[0].percent_discount
							amount_after_ignore = (classFee.amount*percent_discount)/100
							#------------IF USER HAS ALREADY GOT ANY DISCOUNT AND TRYING TO PAY MORE THAN THAT
							if amount_after_ignore < int(v5['paid_amount']):
								err.append('Error. You have discount on '+ str(classFee.display_name) +' of '+str(percent_discount)+'. you tried to pay more than remaing fees.It\'s not get added in receipt.')
								continue							
						
						#-------------CHECKING IF paid IS NOT GREATER THAN actual AMOUNT
						if classFee.amount < int(v5['paid_amount']):
							err.append('you tried to pay more than actual amount for fees'+str(classFee.display_name)+
								' therefore it is not get added in receipt')
							continue
						
						if v5['token_or_chequeno'] != None or v5['token_or_chequeno'] != '':
							chequeNo = v5['token_or_chequeno']

						receipt_amount += int(v5['paid_amount'])

					#-------------CHECKING IF amount IS VALID THEN CREATE RECEIPT
				if receipt_amount > 0:
					paymet_receipt = DpyPaymentReceipt(receipt_amount=receipt_amount,
						status=1,institute_id=instid)
					paymet_receipt.save()

		#-----------THIS for LOOP IS FOR EVERY FEES OBJECT id IN ONE STUDENT'S OBJECT 
		for k2,v2 in data.items():

			classUser = DpyUsers.objects.get(id=k2)

			#------------THIS loop JOB IS TO CREATE RECORD FOR ALL TRANSACTIONS
			for k3,v3 in v2.items():

				for k4,v4 in v3.items():
					
					classFee = DpyInstituteClassFee.objects.get(id=k3)
					any_transaction = DpyFeeTransaction.objects.all().filter(cycle_slot=k4,
						user_id=k2,institute_class_fee_id=k3)

					#-------------CHECKING IF PAID FEES IS GREATER THAN ACTUAL FEES
					for k5,v5 in v4.items():
						if classFee.amount < int(v5['paid_amount']):
							err.append('you tried to pay more than actual fees amount for '+str(classFee.display_name))
							continue

						#----------CHECKING IF USER GOT ANY PREVIOUS TRANSACTION DONE FOR PARTICULAR FEES CYCLE
						if len(any_transaction) > 0:
							remaining_fee = classFee.amount - int(any_transaction[0].paid_amount)
							#------------IF USER HAS ALREADY PAID THEN CHECKING REMAINING FEES TO BE PAID
							if remaining_fee < int(v5['paid_amount']):
								err.append('Error. You have already paid Rs. '+ str(any_transaction[0].paid_amount) + ' for fees '+str(classFee.display_name)+' this time you tried to pay more than remaing.')
								continue

						fees_ignore = DpyUserFeeIgnore.objects.all().filter(user_id=k2,institute_class_fee_id=k3)
						#----------CHECKING IF USER GOT ANY DISCOUNT ON PARTICULAR FEES OR NOT
						if len(fees_ignore) > 0:
							percent_discount = fees_ignore[0].percent_discount
							amount_after_ignore = (classFee.amount*percent_discount)/100
							#------------IF USER HAS ALREADY GOT ANY DISCOUNT AND TRYING TO PAY MORE THAN THAT
							if amount_after_ignore < int(v5['paid_amount']):
								err.append('Error. You have discount on '+ str(classFee.display_name) +' of '+str(percent_discount)+'. you tried to pay more than remaing fees.Therefore transaction of this fees is neglected.')
								continue					


						#------------SAVING ACTUAL TRANSACTION DATA
						fee_transaction = DpyFeeTransaction(paid_amount=v5['paid_amount'],mop=v5['mop'],cycle=classFee.cycle,
							status=v5['mop'],institute_class_fee_id=k3,
							user_id=k2,receipt_id=paymet_receipt.id,cycle_slot=k4,
							added_by=request.user.id)
						fee_transaction.save()

						success.append('fee transaction for fee '+ str(classFee.display_name)+" added successfully.")

		return Response({"status": True, "message": "Successfull.","data":{'success':success,'error':err}})

	def update_fees_pay(self,request):
		'''
		############################################################
		THIS METHOD WILL UPDATE THE DATA OF transaction TABLE'S status FIELD
		ALSO WILL UPDATE DATA OF receipt TABLE
		@param json - PATCH({"transaction_info":{'transaction_id':{'status':},},"receipt_info"{ 'receipt_id':{'response','chequeNo'}, } } })
		############################################################
		'''	
		success = []
		err = []
		instid = request.GET.get('id')
		data = request.data

		#------------THIS for LOOP WILL UPDATE THE DATA FOR fees_transaction
		for k5,v5 in data['transaction_info'].items():

			q1= DpyFeeTransaction.objects.get(id=k5)
			transaction = DpyFeeTransactionSerializer(q1)

			try:
				fees_in_class = DpyInstituteClassFee.objects.get(id=q1.institute_class_fee_id)
				print('k5'+ str(v5))

				actual_status = int(transaction.data['status'])
				new_status = int(v5['status'])

				if actual_status < new_status:
					err.append('Updation not possible for transaction for fees '+str(fees_in_class.display_name)+' for student '+str(q1.user.first_name))
				elif actual_status==3 and new_status==2:
					err.append('Updation not possible for transaction for fees '+str(fees_in_class.display_name)+' for student '+str(q1.user.first_name))
				elif actual_status==2 and new_status==0:
					err.append('Updation not possible for transaction for fees '+str(fees_in_class.display_name)+' for student '+str(q1.user.first_name))
				elif actual_status==3 and new_status==0:
					err.append('Updation not possible for transaction for fees '+str(fees_in_class.display_name)+' for student '+str(q1.user.first_name))
				else:
					#--------------PERFORMING ACTUAL UPDATE AFTER ALL CONDITIONS MATCH 
					DpyFeeTransaction.objects.filter(id=k5).update(**v5,paid_amount=q1.paid_amount,updated_by=request.user.id)

					update_log(request,'DpyFeeTransaction',k5,transaction,v5)

					success.append('updated successfully  transaction for fees '+str(fees_in_class.display_name)+' for student '+str(q1.user.first_name))

			except Exception as e:
				err.append('error occured updating transaction for fees '+str(fees_in_class.display_name)+' for student '+str(q1.user.first_name))

		#-------------THIS for LOOP WILL UPDATE THE DATA FOR payment_receipt
		for k6,v6 in data['receipt_info'].items():
			q1= DpyPaymentReceipt.objecats.get(id=k6)
			receipt = DpyPaymentReceiptSerializer(q1)

			transaction = DpyFeeTransaction.objects.all().filter(receipt_id=q1.id)
			user_info = DpyUsers.objects.get(id=transaction[0].user_id)

			try:
				print('v6 '+ str(v6))

				#--------------PERFORMING ACTUAL UPDATE
				DpyPaymentReceipt.objects.filter(id=k6).update(**v6,receipt_amount=q1.receipt_amount,status=1,updated_by=request.user.id)

				update_log(request,'DpyPaymentReceipt',k6,receipt,v6)
				success.append('updated successfully for fees receipt of student ' + str(user_info.first_name) +" "+ str(user_info.last_name))
			except Exception as e:
				err.append('error occured updating for fees receipt of student ' + str(user_info.first_name) +" "+ str(user_info.last_name))

		return Response({"status": True, "message": "Successfull.","data":{'success':success,'error':err}})

