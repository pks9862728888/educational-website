from django.contrib.auth import get_user_model

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
