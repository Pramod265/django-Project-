from rest_framework.routers import SimpleRouter
from django.urls import include, path
from . import views
app_name = 'class_user_profiling'

router = SimpleRouter()
router.register(r'class-batch', views.ManageClassBatch, base_name='classbatch')
router.register(r'classuser-by-cid', views.ManageClassUser, base_name='classuser')

urlpatterns = [
    path('timetable/', views.timetable_view, name='timetable'),
    path('add-class/', views.addclass_view, name='addclass'),
    path('class/', views.ManageClass.as_view({'get': 'list', 'post': 'create'}), name='class'),
    path('view-classes/<int:dep_id>', views.class_view, name='viewclasses'),
    path('class-details/<int:dep_id>', views.class_details, name='classdetails'),
    path('class-info/<int:dep_id>/<int:ic_id>', views.classinfo_view, name='classinfo'),
    # path('class-batch/', views.ManageClassBatch.as_view({'get':'list','post':'create','patch':'partial_update'}), name='classbatch'),
    path('session/', views.ManageClassSession.as_view({'get': 'list', 'post': 'create'}), name='session'),
    path('session-sub/', views.ManageClassSessionSubject.as_view({'post':'create','get':'list'}), name='sessionsub'),
    path('session-subuser/', views.ManageClassSessionSubjectUser.as_view(), name='cssuser'),
    path('session-bulksubuser/', views.BulkClassSessionSubjectUser.as_view({'get':'list','post':'create'}), name='bulkcssuser'),
    path('cssuser-by-cid/<int:ic_id>/<int:user_type>', views.cssuser_by_icid),
    # path('classuser-by-cid/', views.ManageClassUser.as_view({'get':'list'}), name='classuser'),
    path('departments/', views.ManageDepartments.as_view(), name='dept'),
    path('view-departments/', views.department_view, name='viewdept'),
    path('manage-timetable/', views.ManageTimeTable.as_view(), name='managett'),
    path('manage-lecture/<int:pk>', views.lecture_detail, name='managelec'),
    path('attendance/', views.ManageClassPresentie.as_view({'get': 'list'}),  name='attendance'),
    path('day-attendance/', views.ManageUserDayPresentie.as_view({'get': 'list', 'post': 'create'}),  name='dayattendance'),
    path('', include(router.urls)),
]
