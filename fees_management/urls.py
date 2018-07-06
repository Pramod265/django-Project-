from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework_swagger.views import get_swagger_view
from login import views as login_views
app_name = 'fees_management'

urlpatterns = [
    path('add_fee/', views.add_fee,name='add_fee'),
    path('fee_types/', views.fee_types,name='fee_types'),
    
    # url(r'^student_profile/(?P<id>\d+)/$',views.student_profile,name='student_profile'),
    # url(r'^update_student_profile/(?P<id>\d+)/$',views.update_student_profile,name='update_student_profile'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)