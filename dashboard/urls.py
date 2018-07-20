from django.urls import include, path
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from dmkpython import settings
app_name = 'dashboard'

urlpatterns = [
    path('home/', views.home_view,name='home'),
    path('profile/', views.profile_view,name='profile'),
    # url(r'^bulk_upload/', views.bulk_upload,name='bulk_upload'),
    # url(r'^download/',views.download,name='download'),
    path('profile-edit/', views.profile_edit,name='profile_edit'),
    path('reset_profile/', views.reset_profile,name='reset_profile'),
    path('update_password/', views.update_password,name='update_password'),
    url(r'^student_profile/(?P<id>\d+)/$',views.student_profile,name='student_profile'),
    # url(r'^update_student_profile/(?P<id>\d+)/$',views.update_student_profile,name='update_student_profile'),
    url(r'^update_student_personal/(?P<id>\d+)/$',views.update_student_personal,name='update_student_personal'),
    url(r'^update_student_other/(?P<id>\d+)/$',views.update_student_other,name='update_student_other'),
    # url(r'^register_students/',views.register_students,name='register_students'),
    url(r'^view_students/',views.view_students,name='view_students'),
    url(r'^update_profile/',views.update_profile,name='update_profile'),
    # url(r'^feedback/', views.feedback, name='feedback'),
    # url(r'^update_profile/',views.update_profile,name='update_profile'),
    url(r'^incomplete_student/',views.incomplete_student,name='incomplete_student'),
    url(r'^feedback/', views.feedback, name='feedback'),
 ]# + static(settings.production.MEDIA_URL, document_root=settings.production.MEDIA_ROOT)