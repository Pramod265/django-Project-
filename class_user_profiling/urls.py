from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views
app_name = 'class_user_profiling'

router = DefaultRouter()

urlpatterns = [
    path('timetable/', views.timetable_view, name='timetable'),
    path('add-class/', views.addclass_view, name='addclass'),
    path('class/', views.ManageClass.as_view(), name='class'),
    path('view-classes/<int:dep_id>', views.class_view, name='viewclasses'),
    path('class-details/<int:dep_id>', views.class_details, name='classdetails'),
    path('class-info/<int:dep_id>/<int:ic_id>', views.classinfo_view, name='classinfo'),
    path('session/', views.ManageClassSession.as_view({'get': 'list', 'post': 'create'}), name='session'),
    path('session-sub/', views.ManageClassSessionSubject.as_view(), name='sessionsub'),
    path('session-subuser/', views.ManageClassSessionSubjectUser.as_view(), name='cssuser'),
    path('cssuser-by-cid/<int:ic_id>/<int:user_type>', views.user_by_icid),
    path('departments/', views.ManageDepartments.as_view(), name='dept'),
    path('view-departments/', views.department_view, name='viewdept'),
    path('subject-by-class/<int:ic_id>', views.subject_by_class, name='subbyclass'),
    path('manage-timetable/', views.ManageTimeTable.as_view(), name='managett'),
    path('manage-lecture/<int:pk>', views.lecture_detail, name='managelec'),
    path('attendance/', views.ManageClassPresentie.as_view({'get': 'list'}),  name='attendance'),
]

# router.register(r'^sem/', views.ManageClassSession,base_name='sem')

# urlpatterns += router.urls
