from rest_framework.response import Response
from onboarding.serializers import UserDetails
from onboarding.models import DpyUsers, DpyInstituteUsers
from django.core.serializers import serialize
from django.http import JsonResponse
from rest_auth.models import TokenModel

def user_info(request):
    import json
  # return {'remote_ip': request.META['REMOTE_ADDR']}
    if request.user.is_authenticated:
        queryset = TokenModel.objects.get(user_id=request.user.id)
        mycontext = {}
        
        if 'institute_id' in request.session:
            mycontext = {'institute_id': request.session['institute_id']};
        else:
            instuser = DpyInstituteUsers.objects.get(user_id=request.user.id)
            request.session['institute_id'] = instuser.institute_id

        serializer = UserDetails(queryset,context=mycontext)
        request.session['user_info'] = serializer.data

        return { "user_info" : serializer.data }
    return { "user_info" : []}