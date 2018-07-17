from django.contrib import admin
from .models import DpyDepartment, DpyInstituteClass

# Register your models here.

admin.site.register(DpyDepartment)
admin.site.register(DpyInstituteClass)