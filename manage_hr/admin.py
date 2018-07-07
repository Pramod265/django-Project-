from django.contrib import admin
from .models import DpyEmployee
from .models import Leave
# Register your models here.
admin.site.register(Leave)
admin.site.register(DpyEmployee)