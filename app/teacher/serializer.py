from rest_framework import serializers

from core.models import Subject, Classroom


class CreateClassroomSerializer(serializers.ModelSerializer):
    """Serializer class for creating a new classroom"""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Classroom
        fields = ('id', 'user', 'name')
        read_only_fields = ('id', )


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer class for creating a new subject"""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    classroom = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Classroom.objects.all(),
        required=True
    )

    class Meta:
        model = Subject
        fields = ('id', 'user', 'classroom', 'name')
        read_only_fields = ('id', )
