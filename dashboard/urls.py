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
    url(r'^find_college/',views.find_college,name='find_college'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)