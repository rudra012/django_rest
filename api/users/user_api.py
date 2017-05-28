from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from base import response
from . import serializers


class AuthViewSet(GenericViewSet):
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        print(self.action)
        serializer_class = serializers.UserRegisterSerializer
        if self.action == 'registration':
            serializer_class = serializers.UserRegisterSerializer
        if self.action == 'login':
            serializer_class = serializers.UserLoginSerializer
        return serializer_class

    @list_route(methods=['POST'])
    def register(self, request):
        serializer = serializers.UserRegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user.is_active:
            return response.Created(serializers.UserTokenSerializer(user, context={'request': request}).data)
        return response.Created({"success": "Account successfully created."})

    @list_route(methods=['POST'])
    def login(self, request):
        serializer = serializers.UserLoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
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
        print("Fsdfs")
        return response.Ok(serializers.UserSerializer(self.request.user, context={'request': self.request}).data)
