from .import views
from django.conf.urls import url,include 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name='manage_hr'

urlpatterns = [
    url(r'^$', views.home , name="home"),
    url(r'^home/$', views.home),
    url(r'^leave/$', views.leave, name="leave"),
    url(r'^insert_emp/$', views.insert_emp, name='insert_emp'),
    url(r'^leave/addleave/$', views.addleave, name='addleave'),
    url(r'^leave/numleave/$', views.numleave, name='numleave'),
]

urlpatterns += staticfiles_urlpatterns()