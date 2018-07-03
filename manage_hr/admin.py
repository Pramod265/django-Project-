from django.contrib import admin
from .models import Employee
from .models import Leave
# Register your models here.
admin.site.register(Leave)
admin.site.register(Employee)