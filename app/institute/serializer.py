from rest_framework import serializers

from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin

from core.models import Institute, InstituteProfile, InstituteLogo,\
                        InstituteBanner, InstituteAdmin, InstituteStaff,\
                        InstituteFaculty


class InstituteLogoPictureOnlySerializer(serializers.ModelSerializer):
    """Serializer for getting institute logo only"""
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = InstituteLogo
        fields = ('image', )
        read_only_fields = ('image', )


class InstituteBannerPictureOnlySerializer(serializers.ModelSerializer):
    """Serializer for getting institute banner only"""
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = InstituteBanner
        fields = ('image', )
        read_only_fields = ('image', )


class InstituteProfileMinDetailsSerializer(serializers.ModelSerializer):
    """Serializer for getting min details by teacher"""

    class Meta:
        model = InstituteProfile
        fields = ('motto', 'email', 'phone', 'website_url',
                  'recognition', 'state', )
        read_only_fields = ('motto', 'email', 'phone', 'website_url',
                            'recognition', 'state',)


class InstituteMinDetailsSerializer(CountryFieldMixin,
                                    serializers.ModelSerializer):
    """Serializer for getting min details by the teacher"""
    institute_logo = serializers.SerializerMethodField()
    institute_profile = InstituteProfileMinDetailsSerializer()
    country = CountryField()
    institute_statistics = serializers.SerializerMethodField()

    class Meta:
        model = Institute
        fields = ('id', 'user', 'name', 'country', 'institute_category',
                  'created_date', 'institute_slug', 'institute_profile',
                  'institute_logo', 'institute_statistics')
        read_only_fields = ('user', 'name', 'country', 'institute_category',
                            'created_date', 'institute_slug', 'institute_profile',
                            'institute_logo', 'institute_statistics')

    def get_institute_logo(self, instance):
        """Returns the active logo of the institute"""
        institute_logo_instances = instance.institute_logo.filter(
            active=True)
        try:
            data = dict(InstituteLogoPictureOnlySerializer(
                institute_logo_instances, many=True).data[0])
            image = self.context['request'].build_absolute_uri(data['image'])
            return {
                'image': image,
            }
        except Exception:
            return {}

    def get_institute_statistics(self, instance):
        """Finds and returns institute statistics"""
        return {
            'no_of_students': 0,
            'no_of_faculties': 0,
            'no_of_staff': 0
        }


class InstituteProfileSerializer(serializers.ModelSerializer):
    """Serializer class for creating institute profile"""

    class Meta:
        model = InstituteProfile
        fields = ('motto', 'email', 'phone', 'website_url',
                  'state', 'pin', 'address', 'recognition',
                  'primary_language', 'secondary_language',
                  'tertiary_language')


class CreateInstituteSerializer(CountryFieldMixin,
                                serializers.ModelSerializer):
    """Serializer class for creating institute by teacher"""
    institute_profile = InstituteProfileSerializer(required=True)
    country = CountryField(default='IN')
    url = serializers.SerializerMethodField()

    class Meta:
        model = Institute
        fields = ('name', 'country', 'institute_category',
                  'institute_slug', 'institute_profile', 'url')
        read_only_fields = ('institute_slug', )

    def create(self, validated_data):
        """Create method for saving nested fields"""
        institute_profile = validated_data.pop('institute_profile', None)
        user = self.context['user']
        institute = Institute.objects.create(user=user, **validated_data)

        if institute:
            profile = InstituteProfile.objects.get(institute=institute)
            profile.motto = institute_profile.get('motto', '')
            profile.email = institute_profile.get('email', '')
            profile.phone = institute_profile.get('phone', '')
            profile.website_url = institute_profile.get('website_url', '')
            profile.state = institute_profile.get('state', '')
            profile.pin = institute_profile.get('pin', '')
            profile.address = institute_profile.get('address', '')
            profile.recognition = institute_profile.get('recognition', '')
            profile.primary_language = institute_profile.get(
                'primary_language', profile.primary_language)
            profile.secondary_language = institute_profile.get(
                'secondary_language', '')
            profile.tertiary_language = institute_profile.get(
                'tertiary_language', '')
            profile.save()
            profile.refresh_from_db()
            setattr(institute, 'institute_profile', profile)

        return institute

    def get_url(self, instance):
        """Generates and returns the url of the created profile"""
        return self.context['request'].build_absolute_uri(
            instance.get_absolute_url())


class FullInstituteProfileSerializer(serializers.ModelSerializer):
    """Serializer class for creating institute profile"""

    class Meta:
        model = InstituteProfile
        fields = ('motto', 'email', 'phone', 'website_url',
                  'state', 'pin', 'address', 'recognition',
                  'primary_language', 'secondary_language',
                  'tertiary_language')
        read_only_fields = ('motto', 'email', 'phone',
                            'website_url', 'state', 'pin', 'address',
                            'recognition', 'primary_language',
                            'secondary_language', 'tertiary_language')


class InstituteFullDetailsSerializer(serializers.ModelSerializer):
    """Serializer class for showing full details of the institute"""
    institute_profile = FullInstituteProfileSerializer(read_only=True)
    institute_logo = serializers.SerializerMethodField()
    institute_banner = serializers.SerializerMethodField()
    institute_statistics = serializers.SerializerMethodField()
    country = CountryField()

    class Meta:
        model = Institute
        fields = ('user', 'name', 'country', 'institute_category',
                  'institute_slug', 'created_date', 'institute_profile',
                  'institute_statistics', 'institute_logo', 'institute_banner')
        read_only_fields = ('user', 'name', 'country', 'institute_category',
                            'institute_slug', 'created_date', 'institute_profile',
                            'institute_statistics', 'institute_logo', 'institute_banner')

    def get_institute_logo(self, instance):
        """Returns the active logo of the institute"""
        institute_logo_instances = instance.institute_logo.filter(
            active=True)
        try:
            data = dict(InstituteLogoPictureOnlySerializer(
                institute_logo_instances, many=True).data[0])
            image = self.context['request'].build_absolute_uri(data['image'])
            return {
                'image': image,
            }
        except Exception:
            return {}

    def get_institute_banner(self, instance):
        """Returns the active banner of the institute"""
        institute_banner_instances = instance.institute_banner.filter(
            active=True)
        try:
            data = dict(InstituteBannerPictureOnlySerializer(
                institute_banner_instances, many=True).data[0])
            image = self.context['request'].build_absolute_uri(data['image'])
            return {
                'image': image,
            }
        except Exception:
            return {}

    def get_institute_statistics(self, instance):
        """Finds and returns institute statistics"""
        return {
            'no_of_admin': 1,
            'no_of_students': 0,
            'no_of_faculties': 0,
            'no_of_staff': 0
        }


class InstituteAdminAddSerializer(serializers.ModelSerializer):
    """Serializer for adding admin for institute"""

    class Meta:
        model = InstituteAdmin
        fields = ('institute', 'inviter', 'invitee')


class InstituteStaffAddSerializer(serializers.ModelSerializer):
    """Serializer for adding admin for institute"""

    class Meta:
        model = InstituteStaff
        fields = ('institute', 'inviter', 'invitee')
