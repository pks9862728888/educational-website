from rest_framework import serializers

from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin

from core import models


class InstituteLicenseListSerializer(serializers.ModelSerializer):
    """Serializer for getting list of institute licenses"""

    class Meta:
        model = models.InstituteCommonLicense
        fields = ('id', 'billing', 'type', 'price', 'discount_percent', 'gst_percent',
                  'no_of_admin', 'no_of_staff', 'no_of_faculty',
                  'no_of_student', 'no_of_board_of_members', 'video_call_max_attendees',
                  'classroom_limit', 'department_limit',
                  'subject_limit', 'scheduled_test', 'discussion_forum',
                  'LMS_exists', 'CMS_exists')
        read_only_fields = ('id', 'billing', 'type', 'price', 'discount_percent',
                            'gst_percent', 'no_of_admin', 'no_of_staff',
                            'no_of_faculty', 'no_of_student', 'no_of_board_of_members',
                            'video_call_max_attendees', 'classroom_limit',
                            'department_limit', 'subject_limit',
                            'scheduled_test', 'discussion_forum', 'LMS_exists', 'CMS_exists')


class InstituteLogoPictureOnlySerializer(serializers.ModelSerializer):
    """Serializer for getting institute logo only"""
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = models.InstituteLogo
        fields = ('image', )
        read_only_fields = ('image', )


class InstituteBannerPictureOnlySerializer(serializers.ModelSerializer):
    """Serializer for getting institute banner only"""
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = models.InstituteBanner
        fields = ('image', )
        read_only_fields = ('image', )


class InstituteProfileMinDetailsSerializer(serializers.ModelSerializer):
    """Serializer for getting min details by teacher"""

    class Meta:
        model = models.InstituteProfile
        fields = ('motto', 'email', 'phone', 'website_url',
                  'recognition', 'state', )
        read_only_fields = ('motto', 'email', 'phone', 'website_url',
                            'recognition', 'state',)


class InstituteMinDetailsStudentSerializer(CountryFieldMixin,
                                           serializers.ModelSerializer):
    """Serializer for getting min details of self institute by the student"""
    institute_logo = serializers.SerializerMethodField()
    institute_profile = InstituteProfileMinDetailsSerializer()
    country = CountryField()
    institute_statistics = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = models.Institute
        fields = ('id', 'name', 'country', 'role',
                  'institute_category', 'type', 'created_date',
                  'institute_slug', 'institute_profile',
                  'institute_logo', 'institute_statistics')
        read_only_fields = ('name', 'country', 'institute_category',
                            'type', 'created_date', 'institute_slug', 'role',
                            'institute_profile', 'institute_logo',
                            'institute_statistics')

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
        institute_permissions = models.InstitutePermission.objects.filter(
            institute=instance.pk,
            active=True
        )
        institute_students = models.InstituteStudents.objects.filter(
            institute__pk=instance.pk,
            active=True
        ).count()
        return {
            'no_of_students': institute_students,
            'no_of_faculties': institute_permissions.filter(
                role=models.InstituteRole.FACULTY).count(),
            'no_of_staff': institute_permissions.filter(
                role=models.InstituteRole.STAFF).count(),
            'no_of_admin': institute_permissions.filter(
                role=models.InstituteRole.ADMIN).count()
        }

    def get_role(self, instance):
        """Returns role as student"""
        return 'Student'


class InstituteMinDetailsSerializer(CountryFieldMixin,
                                    serializers.ModelSerializer):
    """Serializer for getting min details of self institute by the teacher"""
    institute_logo = serializers.SerializerMethodField()
    institute_profile = InstituteProfileMinDetailsSerializer()
    country = CountryField()
    institute_statistics = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = models.Institute
        fields = ('id', 'name', 'country', 'role',
                  'institute_category', 'type', 'created_date',
                  'institute_slug', 'institute_profile',
                  'institute_logo', 'institute_statistics')
        read_only_fields = ('name', 'country', 'institute_category',
                            'type', 'created_date', 'institute_slug', 'role',
                            'institute_profile', 'institute_logo',
                            'institute_statistics')

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
        institute_permissions = models.InstitutePermission.objects.filter(
            institute=instance.id,
            active=True
        )
        institute_students = models.InstituteStudents.objects.filter(
            institute__pk=instance.pk,
            active=True
        ).count()
        return {
            'no_of_students': institute_students,
            'no_of_faculties': institute_permissions.filter(
                role=models.InstituteRole.FACULTY).count(),
            'no_of_staff': institute_permissions.filter(
                role=models.InstituteRole.STAFF).count(),
            'no_of_admin': institute_permissions.filter(
                role=models.InstituteRole.ADMIN).count()
        }

    def get_role(self, instance):
        """Returns role of the teacher"""
        return models.InstitutePermission.objects.filter(
            institute=instance,
            invitee=self.context['user'],
            active=True
        ).first().role


class InstitutePendingInviteMinDetailsSerializer(CountryFieldMixin,
                                                 serializers.ModelSerializer):
    """Serializer for getting pending invites min details by the teacher"""
    institute_logo = serializers.SerializerMethodField()
    institute_profile = InstituteProfileMinDetailsSerializer()
    country = CountryField()
    institute_statistics = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    invited_by = serializers.SerializerMethodField()

    class Meta:
        model = models.Institute
        fields = ('id', 'name', 'country', 'role', 'type',
                  'invited_by', 'institute_category', 'created_date',
                  'institute_slug', 'institute_profile',
                  'institute_logo', 'institute_statistics')
        read_only_fields = ('user', 'name', 'country', 'institute_category',
                            'type', 'created_date', 'institute_slug', 'role',
                            'invited_by', 'institute_profile',
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
        institute_permissions = models.InstitutePermission.objects.filter(
            institute=instance.id,
            active=True
        )
        return {
            'no_of_students': 0,
            'no_of_faculties': institute_permissions.filter(
                role=models.InstituteRole.FACULTY).count(),
            'no_of_staff': institute_permissions.filter(
                role=models.InstituteRole.STAFF).count(),
            'no_of_admin': institute_permissions.filter(
                role=models.InstituteRole.ADMIN).count()
        }

    def get_role(self, instance):
        """Returns role of the teacher"""
        return models.InstitutePermission.objects.filter(
            institute=instance,
            invitee=self.context['user'],
            active=False
        ).first().role

    def get_invited_by(self, instance):
        """Returns the email of the inviter"""
        return str(models.InstitutePermission.objects.filter(
            institute=instance,
            invitee=self.context['user'],
            active=False
        ).first().inviter)


class InstitutesJoinedMinDetailsTeacher(CountryFieldMixin,
                                        serializers.ModelSerializer):
    """Serializer for getting joined institutes min details by the teacher"""
    institute_logo = serializers.SerializerMethodField()
    institute_profile = InstituteProfileMinDetailsSerializer()
    country = CountryField()
    institute_statistics = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = models.Institute
        fields = ('id', 'name', 'country', 'role',
                  'institute_category', 'type', 'created_date',
                  'institute_slug', 'institute_profile',
                  'institute_logo', 'institute_statistics')
        read_only_fields = ('user', 'name', 'country', 'institute_category',
                            'type', 'created_date', 'institute_slug', 'role',
                            'institute_profile', 'institute_logo',
                            'institute_statistics')

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
        institute_permissions = models.InstitutePermission.objects.filter(
            institute=instance.id,
            active=True
        )
        return {
            'no_of_students': 0,
            'no_of_faculties': institute_permissions.filter(
                role=models.InstituteRole.FACULTY).count(),
            'no_of_staff': institute_permissions.filter(
                role=models.InstituteRole.STAFF).count(),
            'no_of_admin': institute_permissions.filter(
                role=models.InstituteRole.ADMIN).count()
        }

    def get_role(self, instance):
        """Returns role of the teacher"""
        return models.InstitutePermission.objects.filter(
            institute=instance,
            invitee=self.context['user'],
            active=True
        ).first().role


class InstituteProfileSerializer(serializers.ModelSerializer):
    """Serializer class for creating institute profile"""

    class Meta:
        model = models.InstituteProfile
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
        model = models.Institute
        fields = ('name', 'country', 'institute_category', 'type',
                  'institute_slug', 'institute_profile', 'url')
        read_only_fields = ('institute_slug', )

    def create(self, validated_data):
        """Create method for saving nested fields"""
        institute_profile = validated_data.pop('institute_profile', None)
        user = self.context['user']
        institute = models.Institute.objects.create(user=user, **validated_data)

        if institute:
            profile = models.InstituteProfile.objects.get(institute=institute)
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
        model = models.InstituteProfile
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
    role = serializers.SerializerMethodField()

    class Meta:
        model = models.Institute
        fields = ('user', 'name', 'country', 'institute_category', 'type',
                  'role', 'institute_slug', 'created_date', 'institute_profile',
                  'institute_statistics', 'institute_logo', 'institute_banner')
        read_only_fields = ('user', 'name', 'country', 'institute_category',
                            'type', 'institute_slug', 'created_date', 'role',
                            'institute_profile', 'institute_statistics',
                            'institute_logo', 'institute_banner')

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

    def get_role(self, instance):
        """Returns role of the teacher"""
        return models.InstitutePermission.objects.filter(
            institute=instance,
            invitee=self.context['user'],
            active=True
        ).first().role


class InstituteProvidePermissionSerializer(serializers.ModelSerializer):
    """Serializer class for providing permission of institute to user"""

    class Meta:
        model = models.InstitutePermission
        fields = ('institute', 'inviter', 'invitee', 'active', 'role',
                  'request_accepted_on')


class InstituteClassSerializer(serializers.ModelSerializer):
    """Serializer for creating institute class"""

    class Meta:
        model = models.InstituteClass
        fields = ('id', 'class_institute', 'name', 'class_slug',
                  'created_on')
        read_only_fields = ('id', 'class_slug', 'created_on')


class SubjectIntroductoryFileMaterialSerializer(serializers.ModelSerializer):
    """Serializer for creating introductory study material"""
    file = serializers.FileField(allow_null=False, use_url=True)

    class Meta:
        model = models.SubjectIntroductoryContent
        fields = ('id', 'view', 'name', 'file', 'can_download', 'content_type')
        read_only_fields = ('id',)


class LectureMaterialSerializer(serializers.ModelSerializer):
    """Serializer for lecture material"""

    class Meta:
        model = models.SubjectLectureMaterials
        fields = ('id', 'lecture', 'content_type', 'name')
        read_only_fields = ('id',)


class SubjectLectureImageSerializer(serializers.ModelSerializer):
    """Serializer for creating image study material"""
    file = serializers.FileField(allow_null=False, use_url=True)
    lecture_material = serializers.PrimaryKeyRelatedField(
        queryset=models.SubjectLectureMaterials.objects.all()
    )

    class Meta:
        model = models.SubjectLectureImageMaterial
        fields = ('id', 'lecture_material', 'file', 'can_download')
        read_only_fields = ('id',)


class SubjectLecturePdfSerializer(serializers.ModelSerializer):
    """Serializer for creating image study material"""
    file = serializers.FileField(allow_null=False, use_url=True)

    class Meta:
        model = models.SubjectLecturePdfMaterial
        fields = ('id', 'lecture_material', 'file', 'can_download')
        read_only_fields = ('id',)
