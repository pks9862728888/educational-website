from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Subject


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer class for creating a new subject"""
    user = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=get_user_model().objects.all(),
        required=True
    )

    class Meta:
        model = Subject
        fields = ('id', 'user', 'name')
        read_only_fields = ('id', )
