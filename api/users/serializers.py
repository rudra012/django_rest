from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from base import services
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password')
        write_only_fields = ('password',)

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class UserTokenSerializer(serializers.ModelSerializer):
    """
    User model with auth token
    """
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'auth_token')
        read_only_fields = ('email', 'auth_token')

    def get_auth_token(self, user_obj):
        return services.get_token_for_user(user_obj, "authentication")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
        read_only_fields = ('id', 'email')


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        fields = ('email', 'password')

    def validate(self, attrs):
        print(attrs)
        # print(attrs.get("email"))
        # print(attrs.get("password"))

        user = authenticate(username=attrs.get("email"), password=attrs.get("password"))
        if not user:
            raise serializers.ValidationError('Email or password incorrect!')
        attrs["user"] = user
        return attrs
