from django.urls import include, path
from . import views

app_name = 'class_user_profiling'

urlpatterns = [
    path('timetable/', views.timetable_view,name='timetable'),
]