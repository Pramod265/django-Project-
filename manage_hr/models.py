from django.db import models
from onboarding.models import DpyInstitute,DpyInstituteUsers,DpyUsers
# Create your models here.
# class (models.Model):
#     institute = models.ForeignKey(DpyInstitute, models.DO_NOTHING)
#     first_name = models.CharField(db_column='First Name', max_length=20)  # Field name made lowercase. Field renamed to remove unsuitable characters.
#     middle_name = models.CharField(db_column='Middle Name', max_length=20)  # Field name made lowercase. Field renamed to remove unsuitable characters.
#     last_name = models.CharField(db_column='Last Name', max_length=20)  # Field name made lowercase. Field renamed to remove unsuitable characters.
#     designation = models.CharField(db_column='Designation', max_length=20)  # Field name made lowercase.
#     department = models.CharField(db_column='Department', max_length=20)  # Field name made lowercase.
#     gender = models.CharField(db_column='Gender', max_length=10)  # Field name made lowercase.
#     date_of_join = models.CharField(db_column='Date of Join', max_length=10)  # Field name made lowercase. Field renamed to remove unsuitable characters.
#     basic_salary = models.IntegerField(db_column='Basic Salary')  # Field name made lowercase. Field renamed to remove unsuitable characters.
#     mobile_number = models.CharField(db_column='Mobile Number', max_length=12)  # Field name made lowercase. Field renamed to remove unsuitable characters.
#     email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
#     casual_leaves = models.CharField(max_length=50)
#     paid_leaves = models.CharField(max_length=50)
#     sick_leaves = models.CharField(max_length=50)
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.IntegerField(default=0)
#     updated_on = models.DateTimeField(auto_now=True)
#     updated_by = models.IntegerField(default=0)

#     class Meta:
#         managed = False
#         db_table = 'dpy_employee'


class Leave(models.Model):
    emp_id = models.IntegerField()
    institute = models.ForeignKey(DpyInstitute, models.PROTECT)
    emp_name = models.CharField(max_length=25)
    leave_type = models.CharField(max_length=25)
    start_date = models.CharField(max_length=25)
    end_date = models.CharField(max_length=25)
    reason = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'dpy_employee_leave'

class DpyLeaveTypes(models.Model):
    # id = models.IntegerField()
    emp = models.ForeignKey(DpyUsers, models.PROTECT)
    institute = models.ForeignKey(DpyInstitute, models.PROTECT)
    leave_name = models.CharField(db_column='Leave_name', max_length=50)  # Field name made lowercase.
    leaves_remaining = models.IntegerField(db_column='Leaves_remaining')  # Field name made lowercase.
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'dpy_leave_types'

class DpyEmployeeSalaryStructure(models.Model):
    emp = models.ForeignKey(DpyUsers, models.PROTECT)
    institute = models.ForeignKey(DpyInstitute, models.PROTECT)
    month = models.CharField(max_length=20)
    year = models.CharField(max_length=20)
    basic = models.IntegerField()
    hra = models.IntegerField()
    ta = models.IntegerField()
    da = models.IntegerField()
    bonus = models.IntegerField()
    spal = models.IntegerField()
    med = models.IntegerField()
    others = models.IntegerField()
    tds = models.IntegerField()
    pf = models.IntegerField()
    pt = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'dpy_employee_salary_structure'

