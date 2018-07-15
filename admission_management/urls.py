from django.urls import include, path
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from dmkpython import settings
app_name = 'admission_management'

urlpatterns = [
    path('admission/', views.admission,name='admission'),
    path('enquiry/', views.enquiry,name='enquiry'),
    path('view_enquiry/', views.view_enquiry,name='view_enquiry'),
    path('view_admission/', views.view_admission,name='view_admission'),
    path('take_enquiry/', views.take_enquiry,name='addenquiry'),
    # path('view_enquiry_details/<int:id>', views.view_enquiry_details,name='viewenquiry'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)