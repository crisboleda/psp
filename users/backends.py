
# Django
from django.conf import settings

# Models
from django.contrib.auth.models import User


class CustomUserAuthentication:

    def authenticate(self, request, username=None, password=None):

        if 'username' in settings.METHOD_USER_AUTHENTICATION and 'email' in settings.METHOD_USER_AUTHENTICATION:
            return self.authenticate_username_email(username, password)

        elif 'username' in settings.METHOD_USER_AUTHENTICATION:
            return self.authenticate_username(username, password)

        else:
            return self.authenticate_email(username, password)
            

    def authenticate_username_email(self, username, password):
        user = self.authenticate_username(username, password)
        if user is None:
            user = self.authenticate_email(username, password)
        return user

    def authenticate_username(self, username, password):
        user = User.objects.get(username=username, password=password)
        return user

    def authenticate_email(self, email, password):
        user = User.objects.get(email=email, password=password)
        return user

