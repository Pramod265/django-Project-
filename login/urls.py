from django.urls import include, path
from rest_auth.views import LoginView, PasswordChangeView
from .views import login_view, LogoutViewEx, CurrentUserView, SetUserInstitute, CheckUserInstitute
app_name = 'login'

urlpatterns = [
    # path('rests-auth/', include('rest_auth.urls'),name='auth_urls'),
    # path('login/', login_view,name='login_view'),
    path('user/', CurrentUserView.as_view(),name='users'),
    path('rest-auth/login/', LoginView.as_view(), name='rest_login', ),
    path('rest-auth/logout/', LogoutViewEx.as_view(), name='rest_logout', ),
    path('rest-auth/change-password/', PasswordChangeView.as_view(), name='rest_pass', ),
    path('set-institute/', SetUserInstitute.as_view(), name='set_institute', ),
    path('check-institute/', CheckUserInstitute.as_view(), name='check_institute', ),
]