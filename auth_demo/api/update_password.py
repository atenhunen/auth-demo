"""Update password API."""
import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from auth_demo.api.serialisers import ChangePasswordSerializer

from auth_demo.api.constants import Status

class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope)
    required_scopes = ['write']

    def get_object(self, queryset=None):
        """Get user object."""
        return self.request.user

    def put(self, request, *args, **kwargs):
        """HTTP PUT. Update password."""
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # set_password hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=Status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=Status.HTTP_400_BAD_REQUEST)