from django.db import models
from onboarding.models import DpyInstitute, DpyUsers
from class_user_profiling.models import DpyDepartment, DpyInstituteClass, DpyInstituteClassSession, DpyInstituteClassSessionSubject
# Create your models here.
	
class DpyFeeType(models.Model):
	desc = models.CharField(max_length=250)
	added_by = models.IntegerField(default=0)
	added_on = models.DateTimeField(auto_now_add=True)
	updated_by = models.IntegerField(default=0)
	updated_on = models.DateTimeField(auto_now_add=True, null=True)
	class Meta:
		managed = True		
		db_table = 'dpy_fee_type'
		verbose_name = "dpy_fee_type"


class DpyInstituteClassFee(models.Model):
	fee_type = models.ForeignKey(DpyFeeType, on_delete=models.PROTECT)
	institute_class = models.ForeignKey(DpyInstituteClass, on_delete=models.PROTECT)
	amount = models.IntegerField() 
	cycle = models.PositiveSmallIntegerField()
	display_name = models.CharField(max_length=250)
	bifurcations = models.TextField(null=True)
	status = models.PositiveSmallIntegerField(default=1)
	added_by = models.IntegerField(default=0)
	added_on = models.DateTimeField(auto_now_add=True)
	updated_by = models.IntegerField(default=0)
	updated_on = models.DateTimeField(auto_now_add=True, null=True)

	class Meta:
		managed = True
		db_table = 'dpy_institute_class_fee'
		verbose_name = "Institute Class Fee"

class DpyUserFeeIgnore(models.Model):
	institute_class_fee = models.ForeignKey(DpyInstituteClassFee,on_delete=models.PROTECT)
	user = models.ForeignKey(DpyUsers,on_delete=models.PROTECT)
	percent_discount=models.FloatField()
	status = models.PositiveSmallIntegerField()
	added_by = models.IntegerField(default=0)
	added_on = models.DateTimeField(auto_now_add=True)
	updated_by = models.IntegerField(default=0)
	updated_on = models.DateTimeField(auto_now_add=True, null=True)
	class Meta:
		managed = True
		db_table = 'dpy_user_fee_ignore'
		verbose_name = "Dpy User Fee Ignore"

class  DpyPaymentReceipt(models.Model):
	institute_id = models.ForeignKey(DpyInstitute,on_delete=models.PROTECT)
	token_or_chequeno = models.TextField(null=True,default=0) #'unique code or gateway reference id in case of online payment'
	response = models.TextField(null=True,default=0)
	mop = models.IntegerField(default=4)
	receipt_amount = models.FloatField()
	status = models.PositiveSmallIntegerField()
	added_by = models.IntegerField(default=0)
	added_on = models.DateTimeField(auto_now_add=True)
	updated_by = models.IntegerField(default=0)
	updated_on = models.DateTimeField(auto_now_add=True, null=True)
	class Meta:
		managed = True
		db_table = 'dpy_payment_receipt'
		verbose_name = "Dpy Payment Receipt"

class DpyFeeTransaction(models.Model):
	user = models.ForeignKey(DpyUsers,on_delete=models.PROTECT)
	institute_class_fee = models.ForeignKey(DpyInstituteClassFee,on_delete=models.PROTECT)
	receipt = models.ForeignKey(DpyPaymentReceipt,on_delete=models.PROTECT)
	paid_amount = models.FloatField()
	cycle = models.IntegerField()
	cycle_slot = models.IntegerField()
	dsc = models.TextField()
	mop = models.IntegerField(default=1) #'1=CASH,2=CHEQUE,3=NEFT/RTGS,4=ONLINE,5=BANK DEPOSITE'
	status = models.PositiveSmallIntegerField(default=1) #'1=Paid,2=Cheque Pending,3=Online Pending,4=Refund'
	added_by = models.IntegerField(default=0)
	added_on = models.DateTimeField(auto_now_add=True)
	updated_by = models.IntegerField(default=0)
	updated_on = models.DateTimeField(auto_now_add=True, null=True)
	class Meta:
		managed = True
		db_table = 'dpy_fee_transaction'
		verbose_name = "Dpy Payment Receipt"