from django.shortcuts import render, redirect
from rest_auth.views import LogoutView
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from onboarding.serializers import InstituteUserSerializer, UserDetails
from onboarding.models import DpyUsers, DpyInstituteUsers
from rest_auth.models import TokenModel
from rest_framework import status

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return render(request, 'login/login.html', { 'form': [] })

class LogoutViewEx(LogoutView):
    authentication_classes = (authentication.TokenAuthentication,)

class CurrentUserView(APIView):
    def get(self, request):
        queryset = TokenModel.objects.get(user_id=self.request.user.id)
        # queryset = DpyUsers.objects.get(pk=self.request.user.id)
        # queryset = DpyInstituteUsers.objects.filter(user_id=self.request.user.id)
        # serializer = InstituteUserSerializer(queryset,many=True)
        serializer = UserDetails(queryset)
        return Response(serializer.data)

class SetUserInstitute(APIView):
    def post(self, request, format=None):
        institute_id = request.data.get('institute_id')
        request.session['institute_id'] = institute_id
        return Response({"status": True, "message": "Institute Set Successfully"}, status=status.HTTP_201_CREATED)

class CheckUserInstitute(APIView):
    def post(self, request, format=None):
        if 'institute_id' not in request.session:
            return Response({"status": False, "message": "Institute not set"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": True, "message": "Institute is set"}, status=status.HTTP_201_CREATED)
