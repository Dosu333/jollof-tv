from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions
from email_validator import validate_email, EmailNotValidError
from .models import Token, User


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'verified',
                   'country', 'state', 'city', 'last_login', 'date_joined']


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for user object"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'verified',
                  'phone', 'country', 'state', 'city', 'last_login', 'date_joined')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8},
                        'last_login': {'read_only': True}}

    def validate(self, attrs):
        email = attrs.get('email', None)
        if email:
            email = attrs['email'].lower().strip()
            try:
                valid = validate_email(attrs['email'])
                attrs['email'] = valid.email
                return super().validate(attrs)
            except EmailNotValidError as e:
                raise serializers.ValidationError(e)
        return super().validate(attrs)
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # user = self.context['request'].user
        instance = super().update(instance, validated_data)
        if validated_data.get('password', False):
            instance.set_password(validated_data.get('password'))
            instance.save()
        return instance


class CustomObtainTokenPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        if not user.verified:
            raise exceptions.AuthenticationFailed(
                _('Account not yet verified.'), code='authentication')
        token = super().get_token(user)
        # Add custom claims
        token.id = user.id
        token['email'] = user.email
        if user.first_name and user.last_name:
            token['fullname'] = user.first_name + ' ' + user.last_name
        token['phone'] = user.phone
        user.save_last_login()
        return token


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        if email:
            user = authenticate(
                request=self.context.get('request'),
                username=email.lower().strip(),
                password=password
            )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs


class InitializePasswordResetSerializer(serializers.Serializer):
    """Serializer for sending password reset email to the user"""
    email = serializers.CharField(required=True)


class CreatePasswordSerializer(serializers.Serializer):
    """Serializer for password change on reset"""
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)