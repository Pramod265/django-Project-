from rest_framework import serializers
from .models import (
	# DpyFeeType,
	DpyInstituteClassFee,
	DpyUserFeeIgnore,
	DpyPaymentReceipt,
	DpyFeeTransaction,
	)

from onboarding.serializers import UserSerializer
from django.forms.models import model_to_dict
from class_user_profiling.models import (
	DpyInstituteClass,
	DpyDepartment,
	)

class DpyInstituteClassForFeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = DpyInstituteClass
		fields = ('id','standard','division','sort_index')

class DpyInstituteClassFeeSerializer(serializers.ModelSerializer):
	# fee_type = DpyFeeTypeSerializer(many=True, read_only=True)
	class Meta:
		model = DpyInstituteClassFee
		fields = ('id','amount','cycle','institute_class','display_name','bifurcations','status')

	# def update(self, instance, validated_data):
	# 	print('this - here')
	# 	demo = DpyInstituteClassFee.objects.get(id=instance)
	# 	DpyInstituteClassFee.objects.filter(id=instance)\
	# 					   .update(**validated_data)
	# 	return demo

class DpyUserFeeIgnoreSerializer(serializers.ModelSerializer):
	class Meta:
		model = DpyUserFeeIgnore
		fields = ('id','percent_discount','status','user','institute_class_fee')

class DpyFeeTransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = DpyFeeTransaction
		fields = ('id','paid_amount','cycle','cycle_slot','dsc','mop','status','institute_class_fee_id','receipt_id',
			'user_id')

class DpyPaymentReceiptSerializer(serializers.ModelSerializer):
	class Meta:
		model = DpyPaymentReceipt
		fields = ('token_or_chequeno','response','mop','receipt_amount','status','institute_id')

