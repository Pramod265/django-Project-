from django.urls import include, path
from rest_auth.views import LoginView
from .views import login_view, LogoutViewEx, CurrentUserView
app_name = 'login'

urlpatterns = [
    # path('rests-auth/', include('rest_auth.urls'),name='auth_urls'),
    # path('login/', login_view,name='login_view'),
    path('user/', CurrentUserView.as_view(),name='users'),
    path('rest-auth/login/', LoginView.as_view(), name='rest_login', ),
    path('rest-auth/logout/', LogoutViewEx.as_view(), name='rest_logout', ),
]