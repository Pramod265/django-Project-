from django.db import models

# Create your models here.
# class DpyStudents(models.Model):
#     first_name = models.CharField(max_length=20)
#     middle_name = models.CharField(max_length=20)
#     last_name = models.CharField(max_length=20)
#     mother_name = models.CharField(max_length=20)
#     date_of_addmission = models.CharField(max_length=20)
#     roll_no = models.IntegerField()
#     gr_no = models.IntegerField()
#     dob = models.CharField(max_length=20)
#     email = models.CharField(max_length=100,null="true")
#     blood_group = models.CharField(max_length=20)
#     caste = models.CharField(max_length=20)
#     nationality = models.CharField(max_length=20)
#     religion = models.CharField(max_length=20)
#     communication_address = models.CharField(max_length=255)
#     permanent_address = models.CharField(max_length=255)
#     adhar_no = models.CharField(max_length=20)
#     house = models.CharField(max_length=20)
#     special_quata = models.CharField(max_length=20)
#     gender = models.CharField(max_length=20)
#     student_type = models.CharField(max_length=20)
#     mobile = models.CharField(max_length=12)
#     student_class = models.CharField(max_length=12,default = "", null=True)
#     section = models.CharField(max_length=12,default = "", null=True)
#     institute_id = models.IntegerField()
#     class Meta:
#         managed = False
#         db_table = 'dpy_students'

class Feedback(models.Model):
    #product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=120)
    email = models.EmailField()
    details = models.TextField()
    phone_no = models.CharField(max_length=12, default='SOME STRING')
    #happy = models.BooleanField()
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return self.customer_name