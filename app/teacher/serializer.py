from rest_framework import serializers

from core.models import Subject


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer class for creating a new subject"""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Subject
        fields = ('id', 'user', 'name')
        read_only_fields = ('id', )
