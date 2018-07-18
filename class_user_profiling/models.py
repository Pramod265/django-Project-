from django.db import models
from onboarding.models import DpyInstitute, DpyUsers


# Create your models here.
class DpyDepartment(models.Model):
    name = models.CharField(max_length=255)
    institute = models.ForeignKey(DpyInstitute, on_delete=models.PROTECT)
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
    department = models.ForeignKey(DpyDepartment,related_name="departments",on_delete=models.PROTECT)
    institute = models.ForeignKey(DpyInstitute, on_delete=models.PROTECT)
    standard = models.CharField(max_length=255)
    division = models.CharField(max_length=100,null=True,blank=True)
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
        return str(self.standard)+str(self.division)


class DpyInstituteClassSession(models.Model):
    ic = models.ForeignKey(DpyInstituteClass, related_name='class_session', on_delete=models.PROTECT)
    start_month = models.PositiveSmallIntegerField()
    end_month = models.PositiveSmallIntegerField()
    prerequisite_session = models.IntegerField(default=0)#Eligibility class_session id (to be first cleared)
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'dpy_class_session'
        verbose_name = "Institute Class Session"

    def __str__(self):
        return str(self.start_month)+str(self.end_month)

class DpyInstituteClassSessionSubject(models.Model):
    cs = models.ForeignKey(DpyInstituteClassSession,related_name='subject', on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    prerequisite_subject = models.IntegerField(default=0)#Eligibility class_subject id (to be first cleared in case of exams) 
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'dpy_class_session_subject'
        verbose_name = "Class Session Subject"


class DpyInstituteClassSessionSubjectUser(models.Model):
    css = models.ForeignKey(DpyInstituteClassSessionSubject, related_name='user', on_delete=models.PROTECT)
    user = models.ForeignKey(DpyUsers,on_delete=models.PROTECT)
    user_type = models.PositiveSmallIntegerField(default=1)#1:Student,2:Teacher
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        unique_together = ('css', 'user','user_type',)
        db_table = 'dpy_class_session_subject_user'
        verbose_name = "Class Session Subject User"


class DpyInstituteAdditionalField(models.Model):
    institute = models.ForeignKey(DpyInstitute, on_delete=models.PROTECT)
    key_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    field_type = models.PositiveSmallIntegerField(default=0)#0:varchar,1:date,2:Int
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'dpy_institute_additional_field'
        verbose_name = "Field"

    def __str__(self):
        return self.name


class DpyInstituteUserAdditionalField(models.Model):
    iaf = models.ForeignKey(DpyInstituteAdditionalField, on_delete=models.PROTECT)
    user = models.ForeignKey(DpyUsers,on_delete=models.PROTECT)
    value = models.CharField(max_length=255)
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'dpy_institute_user_additional_field'
        verbose_name = "Field"

    def __str__(self):
        return self.name


class DpyInstituteUserClass(models.Model):
    user = models.ForeignKey(DpyUsers,on_delete=models.PROTECT)
    ic = models.ForeignKey(DpyInstituteClass, on_delete=models.PROTECT)
    user_type = models.PositiveSmallIntegerField(default=1)#1:Student,2:Teacher
    roll_no = models.CharField(max_length=20,null=True)
    is_class_teacher = models.PositiveSmallIntegerField(default=0)
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user','ic','user_type',)
        db_table = 'dpy_institute_user_class'
        verbose_name = "Institute User Class"


class DpyInstituteTimeTable(models.Model):
    institute = models.ForeignKey(DpyInstitute, on_delete=models.PROTECT)
    css = models.ForeignKey(DpyInstituteClassSessionSubject, on_delete=models.PROTECT)
    user = models.ForeignKey(DpyUsers,on_delete=models.PROTECT)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lecture_no = models.PositiveSmallIntegerField()
    day_id = models.PositiveSmallIntegerField()
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'dpy_institute_time_table'
        verbose_name = "Time Table"


class DpyInstituteClassUserPresenties(models.Model):
    ic = models.ForeignKey(DpyInstituteClass, on_delete=models.PROTECT)
    css = models.ForeignKey(DpyInstituteClassSessionSubject, related_name="subject_info", on_delete=models.PROTECT)
    user = models.ForeignKey(DpyUsers, related_name="user_info", on_delete=models.PROTECT)
    marked_by = models.IntegerField()
    date = models.DateField()
    status = models.PositiveSmallIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'dpy_institute_class_user_presenties'
        verbose_name = "Class User Presenties"

