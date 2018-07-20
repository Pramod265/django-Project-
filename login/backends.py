from onboarding.models import DpyUsers
from django.db.models import Q


class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False


    def get_user(self, user_id):
       try:
          return DpyUsers.objects.get(pk=user_id)
       except DpyUsers.DoesNotExist:
          return None


    def authenticate(self, username, password):
        try:
            user = DpyUsers.objects.get(
                Q(username=username) | Q(email=username) | Q(mobile=username)
            )
        except DpyUsers.DoesNotExist:
            return None

        return user if user.check_password(password) else None