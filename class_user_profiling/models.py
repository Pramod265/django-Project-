from django.db import models
from onboarding.models import DpyInstitute, DpyUsers


# Create your models here.
class DpyDepartment(models.Model):
    name = models.CharField(max_length=255)
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'dpy_department'
        verbose_name = "Department"

    def __str__(self):
        return self.name


class DpyInstituteClass(models.Model):
    department = models.ForeignKey(DpyDepartment, on_delete=models.PROTECT)
    institute = models.ForeignKey(DpyInstitute, on_delete=models.PROTECT)
    standard = models.CharField(max_length=255)
    division = models.CharField(max_length=100)
    batch = models.PositiveSmallIntegerField(default=1)
    sort_index = models.PositiveSmallIntegerField(default=0)
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'dpy_institute_class'
        verbose_name = "Institute Class"

    def __str__(self):
        return self.name


class DpyInstituteClassSession(models.Model):
    ic = models.ForeignKey(DpyInstituteClass, on_delete=models.PROTECT)
    start_month = models.PositiveSmallIntegerField()
    end_month = models.PositiveSmallIntegerField()
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'dpy_class_session'
        verbose_name = "Institute Class Session"

    def __str__(self):
        return self.ic

class DpyInstituteClassSessionSubjects(models.Model):
    cs = models.ForeignKey(DpyInstituteClassSession, on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'dpy_class_session_subject'
        verbose_name = "Class Session Subject"

    def __str__(self):
        return self.cs



# class DpyInstituteUserClass(models.Model):
#     user = models.ForeignKey(DpyUsers,on_delete=models.PROTECT)
#     ic = models.ForeignKey(DpyInstituteClass, on_delete=models.PROTECT)
#     status = models.PositiveSmallIntegerField(default=1)
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.IntegerField(default=0)
#     updated_on = models.DateTimeField(auto_now=True)
#     updated_by = models.IntegerField(default=0)

#     class Meta:
#         db_table = 'dpy_institute_user_class'
#         verbose_name = "Institute User Class"

#     def __str__(self):
#         return self.ic