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

		#------------CHEKING IF WE ARE RECEIVING ANY ARRAY OF SELECTED CLASS ids
		if request.GET.getlist('inst_classes[]'):
			ids = request.GET.getlist('inst_classes[]')
			q1 = DpyInstituteClassFee.objects.all().filter(institute_class__in=ids,status=1,institute_id=instid)
			fees_in_class = DpyInstituteClassFeeSerializer(q1, many=True)

			#-----------HERE CREATING JSON OBJ TO THE GIVEN CLASSES ids
			for value in fees_in_class.data:
				final_data.setdefault(value['institute_class'], []).append(value)
				# print(value)
			return Response({"status": True, "message": "Fee Detail For Selected Class.", "data": final_data})
		else: #-------SINCE WE DID NOT RECIEVED ANY CLASS id ARRAY THEREFORE RETURNG ALL THE FEES

			#-------------THIS FOR IS FOR TAKING ids OF ALL THE CLASSES IN THE INSTITUTE
			class_ids = []
			for one_class in classes:
				class_ids.append(one_class.id)

			print(class_ids)
			q1 = DpyInstituteClassFee.objects.all().filter(institute_class_id__in=class_ids,status=1)
			fees_in_class = DpyInstituteClassFeeSerializer(q1, many=True)
			hierarchy = "Class_id ->classs_details{''},fees_id{'fees Details'}"

			#----------HERE CREATING JSON OBJ TO ALL THE FEES ids
			for value in fees_in_class.data:
				obj = DpyInstituteClass.objects.get(id = value['institute_class'])
				final_data.setdefault(value['institute_class'], {'class_details':{'sort_index':obj.sort_index,'standard':obj.standard,'division':obj.division}}).setdefault(value['id'],{}).update(value)
				# final_data[obj.standard+""+str(obj.division)].update({})
				# print(value['display_name']+"standard:"+str(obj.standard)+",division:"+str(obj.division)+"))")
			return Response({"status": True, "message": "Fee detail for all classes."+hierarchy, "data": final_data})

		return Response({"status": True, "message": "Class fees Data.", "data": fees_in_class})


	def new_fee(self,request):
		'''
		############################################################
		THIS FUNCTIONS CREATES NEW fees AND  IT WILL REQUIRE AN JSON 
		ARRAY obj FROM FRONTEND WHOSE FORMAT IS WRITTEN ON DEMO.JSON 
		############################################################
		'''
		formData = request.data
		# print(formData);
		json_obj = json.dumps(formData)
		err = []
		success = []

		#------------THIS FOR LOOP FETCH EVERY ELEMENT OF ARRAY OF 'fees' OBJ
		for data in formData:
			try:	
				inst_class_fee = DpyInstituteClassFee(amount=int(data['amount']),display_name=data['display_name'],cycle=data['cycle'],bifurcations=data['bifurcations'],institute_class_id=data['institute_class'],added_by=request.user.id)
				inst_class_fee.save()

				#-------------HERE APPENDING success obj WITH SUCCESS MESSAGE 
				success.append(str(data['display_name']) + " Fees added for class " + str(data['institute_class']) + ".")
				# success = str(data['display_name']) + " Fees added for class " + str(data['institute_class']) + "."
			except Exception as e:
				#-------------HERE APPENDING err obj ERROR MESSAGE
				err.append(str(data['display_name']) + " Fees Already Exist for class " + str(data['institute_class']) + ".")
		return Response({"status": True, "message": "Class fees Added.","data":{'success':success,'error':err}})


	def partial_update(self, request):
		'''
		###################################################################
		THIS FUNCTION WILL UPDATE fees DATA,HERE IT WILL REQUIRE JSON ARRAY
		###################################################################
		'''
		data = request.data
		json_obj = json.dumps(data)
		err = []
		success = []
		previousVal = ""
		final_data = {}

		#-------------THIS FOR LOOP FETCH EVERY ELEMENT OF ARRAY OF 'fees' OBJ
		for fee_data in data:
			inst_class = DpyInstituteClass.objects.get(id=fee_data['institute_class'])
		# serialized = DpyInstituteClassFeeSerializer(data['id'],request.data,partial=True)
			
			try:
				q0 = DpyInstituteClassFee.objects.get(id=fee_data['id'])
				fees2 = DpyInstituteClassFeeSerializer(q0)

				#-----------PERFORMING ACTUALL UPDATE HERE
				serialized = DpyInstituteClassFee.objects.filter(id=fee_data['id']).update(**fee_data,updated_by=request.user.id)
				
				#-----------CREATING OBJECT OF FEES FOR STATUS MESSAGE
				q1 = DpyInstituteClassFee.objects.get(id=fee_data['id'])
				fees = DpyInstituteClassFeeSerializer(q1)
				# keys = "bifurcations"
				# print("fees.data['dispplay_name']"+fees.data['display_name'])
				
				#storing the values of fields after update
				# previous_data = {}
				# update_data = {}
				# array = []
				
				# for key,value in fee_data.items():
					
				# 	# print(str(key) +":--"+ str(value))
				# 	keys = key
				# 	print(keys)

				# 	update_data[key]=value
				# 	previous_data[key]=fees2.data[keys]

				# # final_data.setdefault('update_log', {'new':update_data}).setdefault('previous',{}).update(previous_data)
				# final_data['new_val'] = update_data
				# final_data['old_val'] = previous_data

				success.append("fees type "+str(fees.data['display_name'])+" updated for class "+str(inst_class.standard)+""+str(inst_class.division)+".")

				#------------CALLING FUNCTION TO UPDATE LOG DATA 
				update_log(request,'DpyInstituteClassFee',fee_data['id'],fees2,fee_data)

			except Exception as e:
				err.append(str(fees.data['display_name'])+" fees already exist for class " +str(inst_class.standard)+""+str(inst_class.division)+".")

		return Response({"status": True, "message": "Connection successful.","data":{'success':success,'error':err}})
		





