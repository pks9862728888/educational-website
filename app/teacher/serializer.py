from django.contrib.auth import get_user_model
from rest_framework import serializers

from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin

from core.models import TeacherProfile, Subject, Classroom


class TeacherProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """Serializer class for teacher profile"""
    country = CountryField()

    class Meta:
        model = TeacherProfile
        fields = ('first_name', 'last_name', 'gender', 'phone', 'country',
                  'date_of_birth', 'primary_language', 'secondary_language',
                  'tertiary_language', 'image')


class ManageTeacherProfileSerializer(serializers.ModelSerializer):
    """Serializer class for creating, retrieving & updating teacher profile"""
    teacher_profile = TeacherProfileSerializer(many=False, )

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'created_date', 'teacher_profile')
        read_only_fields = ('id', 'email', 'created_date')

    def update(self, instance, validated_data):
        """Add or modify details of user"""
        profile_data = validated_data.pop('teacher_profile', None)
        profile = instance.teacher_profile

        user = super().update(instance, validated_data)
        user.save()

        # Updating profile data is profile data is present
        if profile_data:
            if profile_data.get('first_name', None):
                profile.first_name = profile_data.get(
                    'first_name', profile.first_name)

            if profile_data.get('last_name', None):
                profile.last_name = profile_data.get(
                    'last_name', profile.last_name)

            if profile_data.get('gender', None):
                profile.gender = profile_data.get(
                    'gender', profile.gender)

            if profile_data.get('phone', None):
                profile.phone = profile_data.get(
                    'phone', profile.phone)

            if profile_data.get('country', None):
                profile.country = profile_data.get(
                    'country', profile.country)

            if profile_data.get('date_of_birth', None):
                profile.date_of_birth = profile_data.get(
                    'date_of_birth', profile.date_of_birth)

            if profile_data.get('primary_language', None):
                profile.primary_language = profile_data.get(
                    'primary_language', profile.primary_language)

            if profile_data.get('secondary_language', None):
                profile.secondary_language = profile_data.get(
                    'secondary_language', profile.secondary_language)

            if profile_data.get('tertiary_language', None):
                profile.tertiary_language = profile_data.get(
                    'tertiary_language', profile.tertiary_language)

            if profile_data.get('image', None):
                profile.image = profile_data.get(
                    'image', profile.image)

            profile.save()
            profile.refresh_from_db()

        setattr(instance, 'profile', profile)

        return instance


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
