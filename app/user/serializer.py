from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin

from rest_framework import serializers

from core.models import ProfilePictures, UserProfile


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
        fields = ('id', 'email', 'password', 'username', 'is_active',
                  'is_staff', 'is_student', 'is_teacher')
        read_only_fields = ('id', 'username', 'is_active', 'is_staff',
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


class ListProfilePictureSerializer(serializers.ModelSerializer):
    """Serializer class for listing all profile pictures"""

    class Meta:
        model = ProfilePictures
        fields = ('id', 'image', 'uploaded_on',
                  'public_profile_picture', 'class_profile_picture')
        read_only_fields = ('id', 'image', 'uploaded_on',
                            'public_profile_picture', 'class_profile_picture')


class UploadUserProfilePictureSerializer(serializers.ModelSerializer):
    """Serializer class for showing all profile pictures"""
    image = serializers.ImageField(required=True)

    class Meta:
        model = ProfilePictures
        fields = ('id', 'image', 'uploaded_on',
                  'public_profile_picture', 'class_profile_picture')
        read_only_fields = ('id', 'uploaded_on')


class SetUserProfilePictureSerializer(serializers.ModelSerializer):
    """Serializer class for setting profile picture"""
    id = serializers.IntegerField(required=True)
    uploaded_on = serializers.DateTimeField(required=False)

    class Meta:
        model = ProfilePictures
        fields = ('id', 'image', 'uploaded_on',
                  'public_profile_picture', 'class_profile_picture')


class UserProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """Serializer class for teacher profile"""
    country = CountryField()

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'gender', 'phone', 'country',
                  'date_of_birth', 'primary_language', 'secondary_language',
                  'tertiary_language')


class ProfilePicturesSerializer(serializers.ModelSerializer):
    """Serializer class for profile pictures"""

    class Meta:
        model = ProfilePictures
        fields = ('id', 'image', 'uploaded_on',
                  'class_profile_picture', 'public_profile_picture')


class ManageUserProfileSerializer(serializers.ModelSerializer):
    """Serializer class for creating, retrieving & updating teacher profile"""
    user_profile = UserProfileSerializer()
    profile_pictures = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'created_date',
                  'user_profile', 'profile_pictures')
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
        profile_data = validated_data.pop('user_profile', None)
        validated_data.pop('email', None)
        validated_data.pop('profile_pictures', None)
        validated_data.pop('email', None)
        profile = instance.user_profile

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
