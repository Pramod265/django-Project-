from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import datetime

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# from . import enums


# Create your models here.
class DpyInstitute(models.Model):
    name = models.CharField(max_length=255)
    institute_email = models.EmailField(max_length=100,null=True)
    institute_website = models.CharField(max_length=100,null=True)
    demo_link = models.CharField(max_length=100,blank=True) 
    contact = models.CharField(max_length=12,null=True)
    board = models.CharField(max_length=100,blank=True)
    nature = models.PositiveSmallIntegerField()#1:School,2:College,3:Other
    logo = models.ImageField(default='institute_logo.png', blank=True)
    institute_image = models.ImageField(default='institue_default.png', blank=True)
    medium = models.PositiveSmallIntegerField()
    university = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255,blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    pin_code = models.IntegerField()
    state = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'dpy_institute'
        verbose_name = "Institute"

    def __str__(self):
        return self.name

class DpyUsers(AbstractUser):
    email = models.EmailField(max_length=254, unique=True,null=True)
    middle_name = models.CharField(max_length=75, null=True, blank=True)
    mobile = models.CharField(max_length=16, unique=True,null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=20, choices=(("1", "Male"), ("2", "Female"), ("3", "Other")),null=True)
    blood_group = models.CharField(max_length=5,null=True)
    religion = models.CharField(max_length=75,null=True)
    caste = models.CharField(max_length=75,null=True)
    mother_name = models.CharField(max_length=100,null=True)
    nationality = models.CharField(max_length=75,null=True)
    place_of_birth = models.CharField(max_length=75,null=True)
    address = models.CharField(max_length=255,null=True)
    address2 = models.CharField(max_length=255,null=True)
    image = models.ImageField(default='emp_default.png', blank=True)
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'dpy_user'
        verbose_name = "User"

    def get_full_name(self):
        """
        Required function so Django knows what to use as the users full name.
        """
        middle_name = str(" ")+str(self.middle_name)
        if not self.middle_name: middle_name = str('')
        return str(self.first_name)+str(middle_name)+str(" ")+str(self.last_name)

    def get_short_name(self):
        """
        Required function so Django knows what to use as the users short name.
        """

        return self.first_name

    def __str__(self):
        """What to show when we output an object as a string."""

        return self.email

class DpyInstituteUsers(models.Model):
    user = models.ForeignKey(DpyUsers,on_delete=models.PROTECT)
    institute = models.ForeignKey(DpyInstitute, on_delete=models.PROTECT)
    #Role=> 0:Owner, 1:Director/Dean/Principal, 2:HOD/Manager/Clerk, 3:Teacher, 4:Non-Teaching ,5:Office Associate, 6:House Keeping Staff, 7:Student
    role = models.PositiveSmallIntegerField()
    type = models.PositiveSmallIntegerField(default=0)#1:student,2:teacher
    designation = models.CharField(max_length=100,null=True)
    date_of_joining = models.DateField(null=True)
    date_of_leaving = models.DateField(null=True)
    is_active = models.PositiveSmallIntegerField(default=1)
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'dpy_institute_user'
        verbose_name = "Institute User"
    
    def __str__(self):
        return str(self.institute)+str(" : ")+str(self.user)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# class DpyEmployee(models.Model):
#     institute = models.ForeignKey(DpyInstitute, on_delete=models.PROTECT)
#     auth_user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
#     first_name = models.CharField(max_length=75)
#     middle_name = models.CharField(max_length=75, null=True, blank=True)
#     last_name = models.CharField(max_length=75)
#     email = models.EmailField(max_length=254, unique=True,null=True)
#     mobile = models.CharField(max_length=16, unique=True,null=True)
#     password = models.CharField(max_length=100)
#     image = models.ImageField(default='emp_default.png', blank=True)
    # ENUMS = (("1", "admin"), ("2", "teacher"), ("3", "parent"), ("4", "student"), ("5", "transport_admin"), ("6", "driver"))
    # type = models.CharField(max_length=20, choices=ENUMS)
#     # type = models.CharField(max_length=15,choices=[(tag, tag.value) for tag in enums.EmployeeType])# Choices is a list of Tuple
#     is_admin = models.PositiveSmallIntegerField(default=0)
#     designation = models.CharField(max_length=100)
#     status = models.PositiveSmallIntegerField(default=1)
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.IntegerField()
#     updated_on = models.DateTimeField(auto_now=True)
#     updated_by = models.IntegerField(default=0)

#     class Meta:
#         db_table = 'dpy_employee'

#     def __str__(self):
#         return self.first_name