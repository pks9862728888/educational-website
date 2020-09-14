from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from core import models


class CustomUserAdmin(UserAdmin):

    def activate_accounts(self, request, queryset):
        """Activates selected accounts"""
        queryset.update(is_active=True)

    def deactivate_accounts(self, request, queryset):
        """Deactivates selected accounts"""
        queryset.update(is_active=False)

    def add_staff_permission(self, request, queryset):
        """Adds staff permission to selected accounts"""
        queryset.update(is_staff=True)

    def remove_staff_permission(self, request, queryset):
        """Adds staff permission to selected accounts"""
        queryset.update(is_staff=False)

    activate_accounts.short_description = 'Activate accounts'
    deactivate_accounts.short_description = 'Deactivate accounts'
    add_staff_permission.short_descriptin = 'Add Staff permission'
    remove_staff_permission.short_descriptin = 'Remove Staff permission'

    ordering = ['id']
    list_display = [
        'email', 'username', 'is_superuser', 'is_staff', 'is_active',
        'is_student', 'is_teacher'
    ]
    list_filter = ('is_superuser', 'is_staff', 'is_active',
                   'is_teacher', 'is_student')
    search_fields = ['email', 'username', ]
    actions = [
        activate_accounts,
        deactivate_accounts,
        add_staff_permission,
        remove_staff_permission
    ]
    fieldsets = (
        (
            None,
            {'fields': ('email', 'username', 'password')}
        ),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser',
                        'is_student', 'is_teacher')}
        ),
        (
            _('Important Dates'),
            {'classes': ('collapse',), 'fields': ('last_login', )}
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')
        }),
    )


class CustomUserProfile(admin.ModelAdmin):
    """Customizing the user profile admin page"""
    list_display = ['user', 'first_name', 'last_name',
                    'country', 'phone',
                    'primary_language', 'secondary_language',
                    'tertiary_language']
    search_fields = ['user__username', 'first_name',
                     'last_name', 'country',
                     'primary_language', 'secondary_language',
                     'tertiary_language']
    list_filter = ('country', )
    fieldsets = (
        (
            _('Personal details'),
            {
                'fields': ('first_name', 'last_name', 'gender',
                           'date_of_birth')
            }
        ),
        (
            _('Contact details'),
            {
                'fields': (
                    'phone', 'country'
                )
            }
        ),
        (
            _('Language preferences'),
            {
                'fields': (
                    'primary_language',
                    'secondary_language',
                    'tertiary_language')
            }
        )
    )


class CustomProfilePictures(admin.ModelAdmin):
    model = models.ProfilePictures
    list_display = ['id', 'user', 'uploaded_on',
                    'class_profile_picture', 'public_profile_picture']
    list_filter = ['user__email', ]

    def get_user(self, obj):
        return obj.user.email
    get_user.admin_order_field = 'name'  # Allows column order sorting
    get_user.short_description = 'Email of user'  # Renames column head


class CustomSystemMessages(admin.ModelAdmin):
    model = models.SystemMessage
    list_display = ['receiver_email', 'sender_email', 'seen', 'created_date']
    list_filter = ['receiver__username', ]

    @staticmethod
    def receiver_email(obj):
        return obj.receiver.email

    @staticmethod
    def sender_email(obj):
        return obj.sender.email


class CustomInstituteStatistics(admin.ModelAdmin):
    model = models.InstituteStatistics
    list_display = ['institute', 'storage', 'no_of_admins',
                    'no_of_staffs', 'no_of_faculties', 'class_count',
                    'department_count']
    search_fields = ['institute__name']


class CustomInstituteLicense(admin.ModelAdmin):
    model = models.InstituteLicense
    list_display = ['type', 'billing', 'amount', 'discount_percent']
    list_filter = ['type', 'billing']


class CustomInstituteDiscountCoupon(admin.ModelAdmin):
    model = models.InstituteDiscountCoupon
    list_display = ['coupon_code', 'discount_rs', 'created_date',
                    'expiry_date', 'active']
    list_filter = ['active']


class CustomRazorpayCallback(admin.ModelAdmin):
    model = models.RazorpayCallback
    list_display = ['razorpay_order_id', 'razorpay_payment_id',
                    'razorpay_signature', 'institute_license_order_details']
    search_fields = ['razorpay_order_id', 'razorpay_payment_id']


class CustomRazorpayWebhookCallback(admin.ModelAdmin):
    model = models.RazorpayWebHookCallback
    list_display = ['order_id', 'razorpay_payment_id']
    search_fields = ['order_id', 'razorpay_payment_id']


class CustomInstitute(admin.ModelAdmin):
    model = models.InstituteLicense
    list_display = ['name', 'institute_category', 'type']
    list_filter = ['institute_category', 'type']


class CustomInstituteSelectedLicense(admin.ModelAdmin):
    model = models.InstituteSelectedLicense
    list_display = ['type', 'billing', 'net_amount',
                    'discount_coupon']
    list_filter = ['type', 'billing']


class CustomInstituteLicenseOrderDetails(admin.ModelAdmin):
    model = models.InstituteLicenseOrderDetails
    list_display = ['order_receipt', 'payment_gateway', 'amount',
                    'selected_license', 'order_created_on',
                    'paid', 'active', 'end_date']
    list_filter = ('paid', 'active')
    search_fields = ['order_receipt', 'order_id']


class CustomInstituteProfile(admin.ModelAdmin):
    """Customizing the user profile admin page"""
    list_display = ['institute_name', 'admin_email', 'phone',
                    'state', 'recognition', 'primary_language',
                    'secondary_language', 'tertiary_language']
    search_fields = ['institute_name', 'first_name',
                     'last_name', 'country',
                     'primary_language', 'secondary_language',
                     'tertiary_language']
    list_filter = ('state', 'recognition', 'primary_language')

    @staticmethod
    def admin_email(obj):
        return obj.institute.user

    @staticmethod
    def institute_name(obj):
        return obj.institute.name


class CustomInstituteLogo(admin.ModelAdmin):
    model = models.InstituteLogo
    list_display = ['institute_name', 'admin_name', 'image', 'active']
    list_filter = ['institute__name', ]

    @staticmethod
    def institute_name(obj):
        return obj.institute.name

    @staticmethod
    def admin_name(obj):
        return obj.institute.user


class CustomInstituteBanner(admin.ModelAdmin):
    model = models.InstituteBanner
    list_display = ['institute_name', 'admin_name', 'image', 'active']
    list_filter = ['institute__name', ]

    @staticmethod
    def institute_name(obj):
        return obj.institute.name

    @staticmethod
    def admin_name(obj):
        return obj.institute.user


class CustomInstitutePermission(admin.ModelAdmin):
    model = models.InstitutePermission
    list_display = ['institute_name', 'invitee_email', 'role',
                    'active', 'request_accepted_on']
    list_filter = ['active', 'role', 'institute__name', ]

    @staticmethod
    def institute_name(obj):
        return obj.institute.name

    @staticmethod
    def invitee_email(obj):
        return obj.invitee.email


class CustomInstituteClass(admin.ModelAdmin):
    model = models.InstituteClass
    list_display = ['name', 'class_institute', 'created_on']
    search_fields = ['name', 'class_institute']


# class CustomInstituteSubject(admin.ModelAdmin):
#     model = models.InstituteSubject
#     list_display = ['name', 'type']
#     search_fields = ['name', 'type']
#     list_filter = ['type']


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.InstituteLicense, CustomInstituteLicense)
admin.site.register(models.InstituteSelectedLicense,
                    CustomInstituteSelectedLicense)
admin.site.register(models.InstituteLicenseOrderDetails,
                    CustomInstituteLicenseOrderDetails)
admin.site.register(models.InstituteDiscountCoupon,
                    CustomInstituteDiscountCoupon)
admin.site.register(models.RazorpayCallback,
                    CustomRazorpayCallback)
admin.site.register(models.RazorpayWebHookCallback,
                    CustomRazorpayWebhookCallback)
admin.site.register(models.SystemMessage, CustomSystemMessages)
admin.site.register(models.UserProfile, CustomUserProfile)
admin.site.register(models.ProfilePictures, CustomProfilePictures)
admin.site.register(models.Institute, CustomInstitute)
admin.site.register(models.InstituteStatistics, CustomInstituteStatistics)
admin.site.register(models.InstituteProfile, CustomInstituteProfile)
admin.site.register(models.InstituteLogo, CustomInstituteLogo)
admin.site.register(models.InstituteBanner, CustomInstituteBanner)
admin.site.register(models.InstitutePermission, CustomInstitutePermission)
admin.site.register(models.InstituteClass, CustomInstituteClass)
admin.site.register(models.InstituteSubject)
admin.site.register(models.SubjectBookmarked)
admin.site.register(models.SubjectViewNames)
admin.site.register(models.SubjectViewWeek)
admin.site.register(models.InstituteSubjectStatistics)
admin.site.register(models.InstituteSection)
admin.site.register(models.InstituteClassPermission)
admin.site.register(models.InstituteSectionPermission)

admin.site.register(models.InstituteSubjectPermission)
admin.site.register(models.SubjectIntroductoryContent)
admin.site.register(models.SubjectLecture)
admin.site.register(models.SubjectAdditionalReadingUseCaseLink)
admin.site.register(models.SubjectLectureMaterials)
admin.site.register(models.SubjectLectureImageMaterial)
admin.site.register(models.SubjectLecturePdfMaterial)
admin.site.register(models.SubjectLectureLinkMaterial)
admin.site.register(models.SubjectLectureLiveClass)
admin.site.register(models.SubjectLectureUseCaseObjectives)
admin.site.register(models.SubjectLectureAssignment)

admin.site.register(models.InstituteSubjectCourseContent)
admin.site.register(models.SubjectExternalLinkStudyMaterial)
admin.site.register(models.SubjectImageStudyMaterial)
admin.site.register(models.SubjectVideoStudyMaterial)
admin.site.register(models.SubjectPdfStudyMaterial)

admin.site.register(models.InstituteStudents)
admin.site.register(models.InstituteClassStudents)
admin.site.register(models.InstituteSubjectStudents)
admin.site.register(models.InstituteStudyMaterialPreviewStats)
admin.site.register(models.InstituteBannedStudent)
admin.site.register(models.InstituteClassBannedStudent)
admin.site.register(models.InstituteSubjectBannedStudent)
admin.site.register(models.InstituteLastSeen)
admin.site.register(models.InstituteClassLastSeen)
admin.site.register(models.InstituteSubjectLastSeen)

admin.site.register(models.InstituteSubjectCourseContentQuestions)
admin.site.register(models.InstituteSubjectCourseContentAnswer)
admin.site.register(models.InstituteSubjectCourseContentQuestionUpvote)
admin.site.register(models.InstituteSubjectCourseContentAnswerUpvote)
