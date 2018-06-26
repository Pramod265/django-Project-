from django.urls import include, path
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from dmkpython import settings
app_name = 'dashboard'

urlpatterns = [
    path('home/', views.home_view,name='home'),
    path('profile/', views.profile_view,name='profile'),
    url(r'^bulk_upload/', views.bulk_upload,name='bulk_upload'),
    url(r'^download/',views.download,name='download'),
    url(r'^student_profile/(?P<id>\d+)/$',views.student_profile,name='student_profile'),
    url(r'^update_student_profile/(?P<id>\d+)/$',views.update_student_profile,name='update_student_profile'),
    url(r'^register_students/',views.register_students,name='register_students'),
    url(r'^view_students/',views.view_students,name='view_students'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)