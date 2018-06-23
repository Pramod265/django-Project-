from django.shortcuts import render, redirect
from rest_auth.views import LogoutView
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from onboarding.serializers import InstituteUserSerializer
from onboarding.models import DpyInstituteUsers

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return render(request, 'login/login.html', { 'form': [] })

class LogoutViewEx(LogoutView):
    authentication_classes = (authentication.TokenAuthentication,)

class CurrentUserView(APIView):
    def get(self, request):
        queryset = DpyInstituteUsers.objects.get(user_id=self.request.user.id)
        serializer = InstituteUserSerializer(queryset)
        return Response(serializer.data)
