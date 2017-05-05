from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny

from base import response
from . import serializers


class AuthViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    @list_route(methods=['POST'])
    def register(self, request):
        serializer = serializers.UserRegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user.is_active:
            return response.Created(serializers.UserTokenSerializer(user, context={'request': request}).data)
        return response.Created({"success": "Account successfully created."})


class CurrentUserViewSet(viewsets.ViewSet):
    filter_backends = ()

    # @list_route(methods=['POST', 'PATCH', 'PUT'])
    # def update(self, request):
    #     serializer = serializers.UserSerializer(data=self.request.data, instance=request.user, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     updated_user = serializer.save()
    #     return response.Ok(serializers.UserSerializer(updated_user, context={'request': request}).data)
    #
    # GET /me
    def list(self, *args, **kwargs):
        return response.Ok(serializers.UserSerializer(self.request.user, context={'request': self.request}).data)
