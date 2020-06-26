from rest_framework import serializers

from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin

from core.models import Institute, InstituteProfile, InstituteLogo


class InstituteLogoPictureOnlySerializer(serializers.ModelSerializer):
    """Serializer for getting institute logo only"""
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = InstituteLogo
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

    class Meta:
        model = Institute
        fields = ('user', 'name', 'country', 'institute_category',
                  'created_date', 'institute_profile', 'institute_logo')
        read_only_fields = ('user', 'name', 'country', 'institute_category',
                            'created_date', 'institute_profile',
                            'institute_logo')

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
