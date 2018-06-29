from django.db import models

# Create your models here.
class DpyStudentsAbsenties(models.Model):
    date = models.CharField(max_length=20)
    student_id = models.IntegerField()
    teacher_id = models.IntegerField()
    status = models.IntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default=0)
    class Meta:
        managed = False
        db_table = 'dpy_students_absenties'
