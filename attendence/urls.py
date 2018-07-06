from django.urls import include, path
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from dmkpython import settings
app_name = 'attendence'

urlpatterns = [
    path('take_attendence/', views.take_attendence,name='take_attendence'),
    path('apply_attendence/', views.apply_attendence,name='apply_attendence'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)