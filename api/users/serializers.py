from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from base import services
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    fb_auth_token = serializers.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password', 'image', 'cover_image', 'fb_auth_token', 'device_id')
        write_only_fields = ('password',)

    def create(self, validated_data):
        fb_data = validated_data.get('fb_data', {})
        validated_data['fb_id'] = fb_data.get('id')
        validated_data['first_name'] = fb_data.get('first_name', '')
        validated_data['last_name'] = fb_data.get('last_name', '')
        validated_data['device_id'] = fb_data.get('device_id', '')

        validated_data['is_active'] = False
        if validated_data.get('email') == fb_data.get('email'):
            validated_data['is_active'] = True

        user = User.objects.create_user(**validated_data)
        if not user.is_active:
            activation_key = services.generate_activation_key(user)
            context = {
                'user': user,
                'activation_key': activation_key,
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS
            }
            try:
                UserClass = user.__class__
                user_objects = UserClass.objects.filter(device_id=validated_data['device_id'])
                if user_objects:
                    user_objects.update(device_id="")
            except:
                pass
            services.send_mail('registration/activation_email_subject.txt',
                               'registration/activation_email.txt', context,
                               user.email, 'registration/activation_email.html')
        return user


class UserTokenSerializer(serializers.ModelSerializer):
    """
    User model with auth token
    """
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'auth_token', 'fb_id', 'image', 'cover_image')
        read_only_fields = ('email', 'auth_token')

        # def get_auth_token(self, obj):
        #     return services.get_token_for_user(obj, "authentication")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
        read_only_fields = ('id', 'email')
