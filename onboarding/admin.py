from django.contrib import admin
from .models import DpyInstitute, DpyUsers, DpyInstituteUsers

# Register your models here.

admin.site.register(DpyInstitute)
admin.site.register(DpyInstituteUsers)