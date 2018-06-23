from rest_framework.response import Response
from onboarding.serializers import UserSerializer, InstituteUserSerializer
from onboarding.models import DpyUsers, DpyInstituteUsers
from django.core.serializers import serialize
from django.http import JsonResponse

def user_info(request):
    import json
  # return {'remote_ip': request.META['REMOTE_ADDR']}
    if request.user.is_authenticated:
        queryset = DpyInstituteUsers.objects.get(user_id=request.user.id)
        # queryset = DpyUsers.objects.get(pk=self.request.user.id)
        serializer = InstituteUserSerializer(queryset)
        request.session['user_info'] = serializer.data
        return { "user_info" : serializer.data }
    return { "user_info" : []}