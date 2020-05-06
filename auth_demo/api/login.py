"""Login view."""
import requests
import auth_demo.models.utils

from rest_framework import generics
from django.conf import settings
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from auth_demo.models.user import User
from auth_demo.api.serialisers import AccessTokenSerializer
from oauth2_provider.models import Application
from requests.auth import HTTPBasicAuth


class Login(generics.RetrieveAPIView):
    """Django REST API for activating registered users."""
    permission_classes = []
    required_scopes = []
    queryset = []
    serializer_class = AccessTokenSerializer

    def post(self, request, *args, **kwargs):
        """HTTP GET, sends mail

        :param request: Django WSGI request.
        :param args: args
        :param kwargs: kwargs
        """
        data = request._data
        email = data["email"]
        user = auth_demo.models.utils.get_if_exists(
            User, email=email)
        if user is None:
            return HttpResponse("Unknown user")

        password = data["password"]
        data = {
            "grant_type": "password",
            "username": email,
            "password": password}
        app = Application.objects.filter(id=1).first()
        client_id = app.client_id
        client_secret = app.client_secret
        auth = HTTPBasicAuth(client_id, client_secret)
        url = settings.OAUTH2_PROVIDER_LOGIN_URL
        response = requests.post(url, data=data, auth=auth, verify=False)
        resp = response.json()
        access_token = resp.get("access_token", None)
        if access_token is None:
            return Response({"message": "Authentication failed"})
        return Response({"message": "Access granted", "access_token": access_token})
