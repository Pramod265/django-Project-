from django.contrib import admin
from .models import DpyEmployeeSalaryStructure,DpyLeaveTypes
from .models import Leave
# Register your models here.
admin.site.register(Leave)
admin.site.register(DpyEmployeeSalaryStructure)
admin.site.register(DpyLeaveTypes)
