from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer class for creating a new user"""
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password',
                  'is_active', 'is_staff', 'is_teacher', 'is_student')
        read_only_fields = ('is_active', 'is_staff')

    def create(self, validated_data):
        """Create a new user with encrypted password and return it."""
        return get_user_model().objects.create_user(**validated_data)


class LoginUserSerializer(serializers.Serializer):
    """Serializer class for authenticating user"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'username', 'is_active',
                  'is_staff', 'is_student', 'is_teacher')
        read_only_fields = ('username', 'is_active', 'is_staff',
                            'is_student', 'is_teacher')

    def validate(self, attrs):
        """Validates and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with given credentials.')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
