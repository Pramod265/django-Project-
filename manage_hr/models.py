from django.db import models

# Create your models here.
class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    first_name = models.CharField(db_column='First Name', max_length=20)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    middle_name = models.CharField(db_column='Middle Name', max_length=20)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_name = models.CharField(db_column='Last Name', max_length=20)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    designation = models.CharField(db_column='Designation', max_length=20)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=20)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=10)  # Field name made lowercase.
    date_of_join = models.CharField(db_column='Date of Join', max_length=10)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    basic_salary = models.IntegerField(db_column='Basic Salary')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mobile_number = models.CharField(db_column='Mobile Number', max_length=12)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    casual_leaves = models.CharField(max_length=50)
    paid_leaves = models.CharField(max_length=50)
    sick_leaves = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'dpy_employee'
    def __str__(self):
            return self.first_name

class Leave(models.Model):
    emp_id = models.IntegerField()
    emp_name = models.CharField(max_length=25)
    leave_type = models.CharField(max_length=25)
    start_date = models.CharField(max_length=25)
    end_date = models.CharField(max_length=25)
    reason = models.CharField(max_length=200)
    class Meta:
        managed = False
        db_table = 'dpy_employee_leave'

