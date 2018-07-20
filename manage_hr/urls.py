from .import views
from django.conf.urls import url,include 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name='manage_hr'

urlpatterns = [
    url(r'^$', views.home , name="home"),
    url(r'^home/$', views.home),
    url(r'^leave/$', views.leave, name="leave"),
    url(r'^insert_leave/$', views.insert_leave, name="insert_leave"),
    url(r'^salary/$', views.salary, name="salary"),
    url(r'^salary_structure/$', views.salary_structure, name="salary_structure"),
    url(r'^insert_emp/$', views.insert_emp, name='insert_emp'),
    url(r'^leave/addleave/$', views.addleave, name='addleave'),
    url(r'^salary/structure/$', views.structure, name='structure'),
    url(r'^salary_structure/structure/$', views.structure, name='structure'),
    url(r'^salary/slipstructure/$', views.slipstructure, name='slipstructure'),
    url(r'^salary_structure/add_salary_struc/$', views.add_sal_struc, name='add_sal_struc'),
]

urlpatterns += staticfiles_urlpatterns()