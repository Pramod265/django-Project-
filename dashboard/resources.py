from import_export import resources
from .models import DpyStudents
from onboarding.models import DpyUsers
class StudentsResource(resources.ModelResource):
    class Meta:
        model = DpyStudents


class UsersResource(resources.ModelResource):
    class Meta:
        model = DpyUsers