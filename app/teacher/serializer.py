from django.contrib.auth import get_user_model
from rest_framework import serializers

from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin

from core.models import TeacherProfile, ProfilePictures, Subject, Classroom


class TeacherProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """Serializer class for teacher profile"""
    country = CountryField()

    class Meta:
        model = TeacherProfile
        fields = ('first_name', 'last_name', 'gender', 'phone', 'country',
                  'date_of_birth', 'primary_language', 'secondary_language',
                  'tertiary_language')


class ProfilePicturesSerializer(serializers.ModelSerializer):
    """Serializer class for profile pictures"""

    class Meta:
        model = ProfilePictures
        fields = ('id', 'image', 'uploaded_on',
                  'class_profile_picture', 'public_profile_picture')


class ManageTeacherProfileSerializer(serializers.ModelSerializer):
    """Serializer class for creating, retrieving & updating teacher profile"""
    teacher_profile = TeacherProfileSerializer()
    profile_pictures = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'created_date',
                  'teacher_profile', 'profile_pictures')
        read_only_fields = ('id', 'email', 'created_date')

    def get_profile_pictures(self, instance):
        profile_picture_instances = instance.profile_pictures.filter(
            user=instance).filter(class_profile_picture=True)
        try:
            data = dict(ProfilePicturesSerializer(
                profile_picture_instances, many=True).data[0])
            image = self.context['request'].build_absolute_uri(data['image'])
            return {
                'id': data['id'],
                'image': image,
                'uploaded_on': data['uploaded_on'],
                'class_profile_picture': data['class_profile_picture'],
                'public_profile_picture': data['public_profile_picture']
            }
        except Exception:
            return {}

    def update(self, instance, validated_data):
        """Add or modify details of user"""
        profile_data = validated_data.pop('teacher_profile', None)
        validated_data.pop('email', None)
        validated_data.pop('profile_pictures', None)
        validated_data.pop('email', None)
        profile = instance.teacher_profile

        user = super().update(instance, validated_data)
        user.save()

        # Updating profile if profile data is present
        if profile_data:
            profile.first_name = profile_data.get(
                'first_name', '')

            profile.last_name = profile_data.get(
                'last_name', '')

            profile.gender = profile_data.get(
                'gender', '')

            profile.phone = profile_data.get(
                'phone', '')

            if profile_data.get('country', None):
                profile.country = profile_data.get(
                    'country', profile.country)

            profile.date_of_birth = profile_data.get(
                'date_of_birth', '')

            if profile_data.get('primary_language', None):
                profile.primary_language = profile_data.get(
                    'primary_language', profile.primary_language)

            profile.secondary_language = profile_data.get(
                'secondary_language', '')

            profile.tertiary_language = profile_data.get(
                'tertiary_language', '')

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
