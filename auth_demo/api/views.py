import json
import secrets

import auth_demo.models.utils
from urllib.parse import urljoin

from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics, permissions, serializers
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from auth_demo.models.user import User
from auth_demo.api.constants import Status


# first we define the serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )

# Create the API views
class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class RegisterUser(generics.ListCreateAPIView):
    """ Django REST API view for registering new users."""
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []
    #required_scopes = ['write']
    required_scopes = []
    queryset = []
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """HTTP POST, creates new user.

        :param request: Django WSGI request.
        :param args: args
        :param kwargs: kwargs
        """
        print(request._data)
        return create_user(request._data)


def create_user(data):
    """Create new user.

    :param data: user data dictionary.
    :returns: JSON serialized User object or error.
    """
    print(f'Creating user with {data}')
    serialized = UserSerializer(data=data)
    print(vars(serialized))
    email = serialized.initial_data.get('email', None)
    if serialized.is_valid():
        User.objects.create_user(
            email=email,
            username=serialized.initial_data.get(
                'username', serialized.initial_data.get('email', None)),
            first_name=serialized.initial_data.get('first_name', None),
            last_name=serialized.initial_data.get('last_name', None),
            password=serialized.initial_data.get('password', None),
            is_active=False
        )
        link, _ = generate_activation_link(email)
        _send_mail(
            subject="Test server - Please activate you user",
            message=f'Dear user, please activate your user by clicking here {link}.',
            recipients=[email])
        return Response(serialized.data, status=Status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=Status.HTTP_400_BAD_REQUEST)


def _send_mail(subject, recipients, message):
    """Send mail.

    :param subject: Email subject.
    :param recipients: email recipients list ["abc@abc.com", "123@123.com"]
    :param message: Message body.
    """
    print("sending mail")
    if settings.DEBUG_MAIL:
        print("mail in stdout")
        print(subject)
        print(message)
        return
    send_mail(
        subject,
        message,
        'tenhunen.aarno@gmail.com',
        recipients)
    print("Mail sent")


def generate_activation_link(email, hostname=None):
    """Activation link for user"""
    user = auth_demo.models.utils.get_if_exists(User, email=email)
    if user is None:
        return None
    if hostname is None:
        hostname = settings.HOSTNAME
    token = secrets.token_urlsafe(nbytes=9)
    print(f'TOKEN {token}')
    url = urljoin(hostname, f'activate/{token}')
    user.activation_token = token
    user.save()
    return url, token


class Activate(generics.CreateAPIView):
    """Django REST API for activating registered users."""
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []
    # required_scopes = ['write']
    required_scopes = []
    queryset = []
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        """HTTP GET, sends mail

        :param request: Django WSGI request.
        :param args: args
        :param kwargs: kwargs
        """

        user = auth_demo.models.utils.get_if_exists(User, activation_token=kwargs["activation_token"])
        if user is None:
            return Response(
                json.dumps({"status": "Unknown activation token"}),
                status=Status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return Response(
            json.loads('{"status": "OK"}'),
            status=Status.HTTP_200_SUCCESS)

