from auth_demo.models.user import User
from django.shortcuts import get_object_or_404
from auth_demo.api.serialisers import (
    UserSerializer, NonAutheticatedUserSerializer)
from rest_framework import viewsets
from rest_framework.response import Response
from oauth2_provider.models import AccessToken


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = []

    def list(self, request):
        queryset = User.objects.all()
        if authenticate_bearer_token(request):
            serializer = UserSerializer(queryset, many=True)
        else:
            serializer = NonAutheticatedUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_user_or_none(pk=pk)
        if authenticate_bearer_token(request):
            serializer = UserSerializer(user, many=False)
        else:
            serializer = NonAutheticatedUserSerializer(user, many=False)
        return Response(serializer.data)


def authenticate_bearer_token(request):
    """Authenticate bearer token"""

    try:
        token_string = request['_request'].get('HTTP_AUTHORIZATION', None)
        token_clean = token_string.split(' ')[1]
    except Exception:

        token_clean = str(request.auth)
    print(f'request token {token_clean}')
    token = get_token_or_none(token=token_clean)
    if token is None:
        return False
    return True

def get_token_or_none(**filtering):
    return get_object_or_none(AccessToken, **filtering)

def get_user_or_none(**filtering):
    return get_object_or_none(User, **filtering)

def get_object_or_none(model, **filtering):
    try:
        queryset = model.objects.get(**filtering)
    except model.DoesNotExist:
        queryset = None
    return queryset
