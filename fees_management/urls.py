from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .import views
from rest_framework_swagger.views import get_swagger_view
from login import views as login_views
app_name = 'fees_management'

urlpatterns = [
    # path('add_fee/', views.add_fee,name='add_fee'),
    path('fees/', views.Fees.as_view({'post':'new_fee','get':'get_fees','patch':'partial_update'}), name='fees'),
    path('fees_ignore/', views.Fees_ignore.as_view({'post':'new_fees_ignore','get':'get_fees_ignore'}), name='fees_ignore'),
    path('fees_pay/', views.Fees_pay.as_view({'post':'new_fees_pay','get':'get_fees_pay','patch':'update_fees_pay'}), name='fees_pay'),
    path('fee_types/', views.fee_types,name='fee_types'),
    path('pay/', views.pay,name='pay'),
    path('reciept/', views.reciept,name='reciept'),
    path('transaction/', views.transaction,name='transaction'),
    path('updatetrans/', views.updatetrans,name='updatetrans'),
    path('getclass/', views.getclass,name='getclass'),
    # url(r'^student_profile/(?P<id>\d+)/$',views.student_profile,name='student_profile'),
    # url(r'^update_student_profile/(?P<id>\d+)/$',views.update_student_profile,name='update_student_profile'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)