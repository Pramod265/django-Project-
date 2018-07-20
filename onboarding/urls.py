from django.contrib import admin
from django.urls import path, include
from .import views

app_name = 'onboarding'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('add-teacher/', views.AddTeacher.as_view(), name="addteach"),
    path('view-teachers/', views.get_institute_teachers, name="viewteachers"),
    path('add-student/', views.AddStudent.as_view(), name="addstudent"),
]