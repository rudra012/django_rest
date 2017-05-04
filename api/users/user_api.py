from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny

from base import response
from . import serializers


class AuthViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    @list_route(methods=['post'])
    def register(self, request):
        serializer = serializers.UserRegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user.is_active:
            return response.Created(serializers.UserTokenSerializer(user, context={'request': request}).data)
        return response.Created({"success": "Account successfully created."})
