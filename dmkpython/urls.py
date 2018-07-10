"""dmkpython URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view
from login import views as login_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_views.login_view, name='login_view'),
    path('onboarding/', include('onboarding.urls')),
    path('auth/', include('login.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('attendence/', include('attendence.urls')),
    path('fees_management/', include('fees_management.urls')),
    path('manage_hr/', include('manage_hr.urls')),
    path('swagger/', get_swagger_view(title='API Docs'), name='api_docs')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)