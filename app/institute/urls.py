from django.urls import path

from . import views

app_name = 'institute'

urlpatterns = [
    # Institute license related url
    path('get-discount-coupon',
         views.GetInstituteDiscountCouponView.as_view(),
         name='get-discount-coupon'),
    path('institute-license-list',
         views.InstituteLicenseListView.as_view(),
         name="institute-license-list"),
    path('institute-license-detail',
         views.InstituteLicenseDetailView.as_view(),
         name="institute-license-detail"),
    path('select-license',
         views.InstituteSelectLicenseView.as_view(),
         name='select-license'),
    path('create-order',
         views.InstituteCreateOrderView.as_view(),
         name='create-order'),
    path('razorpay-payment-callback',
         views.RazorpayPaymentCallbackView.as_view(),
         name='razorpay-payment-callback'),
    path('razorpay-webhook-callback',
         views.RazorpayWebhookCallbackView.as_view(),
         name='razorpay-webhook-callback'),
    path('<slug:institute_slug>/get-license-purchased',
         views.InstituteLicenseOrderDetailsView.as_view(),
         name='get-license-purchased'),
    path('<slug:institute_slug>/check-license-exists',
         views.InstituteUnexpiredPaidLicenseExistsView.as_view(),
         name='check-license-exists'),
    # Institute related url
    path('create',
         views.CreateInstituteView.as_view(),
         name="create"),
    path('detail/<slug:institute_slug>',
         views.InstituteFullDetailsView.as_view(),
         name="detail"),
    # Institute permission
    path('<slug:institute_slug>/provide-permission',
         views.InstituteProvidePermissionView.as_view(),
         name="provide_permission"),
    path('<slug:institute_slug>/accept-delete-permission',
         views.InstitutePermissionAcceptDeleteView.as_view(),
         name="accept_delete_permission"),
    path('<slug:institute_slug>/<slug:role>/get-user-list',
         views.InstitutePermittedUserListView.as_view(),
         name="get_permission_list"),
    path('institute-min-details-teacher-admin',
         views.InstituteMinDetailsTeacherView.as_view(),
         name="institute-min-details-teacher-admin"),
    path('joined-institutes-teacher',
         views.InstituteJoinedMinDetailsTeacherView.as_view(),
         name="joined-institutes-teacher"),
    path('pending-institute-invites-teacher',
         views.InstitutePendingInviteMinDetailsTeacherView.as_view(),
         name="pending-institute-invites-teacher"),
    # Institute class
    path('<slug:institute_slug>/create-class',
         views.CreateClassView.as_view(),
         name='create-class'),
    path('<slug:class_slug>/delete-class',
         views.DeleteClassView.as_view(),
         name='delete-class'),
    path('<slug:institute_slug>/list-all-class',
         views.ListAllClassView.as_view(),
         name="list-all-class"),
    path('add-class-permission',
         views.ProvideClassPermissionView.as_view(),
         name='add-class-permission'),
    path('<slug:class_slug>/list-class-incharges',
         views.ListPermittedClassInchargeView.as_view(),
         name='list-class-incharges'),
    path('<slug:class_slug>/has-class-perm',
         views.CheckClassPermView.as_view(),
         name='has-class-perm'),
    # Institute subject
    path('<slug:class_slug>/create-subject',
         views.CreateSubjectView.as_view(),
         name='create-subject'),
    path('<slug:class_slug>/list-all-subject',
         views.ListAllSubjectView.as_view(),
         name='list-all-subject'),
    path('add-subject-permission',
         views.AddSubjectPermissionView.as_view(),
         name='add-subject-permission'),
    path('<slug:subject_slug>/list-subject-instructors',
         views.ListSubjectInstructorsView.as_view(),
         name='list-subject-instructors'),
    # Institute subject create course
    path('<slug:subject_slug>/add-subject-course-content',
         views.InstituteSubjectAddCourseContentView.as_view(),
         name='add-subject-course-content'),
    path('<slug:subject_slug>/subject-course-content-min-statistics',
         views.InstituteSubjectMinStatisticsView.as_view(),
         name='subject-course-content-min-statistics'),
    path('<slug:subject_slug>/<slug:view_key>/list-subject-specific-view-course-contents',
         views.InstituteSubjectSpecificViewCourseContentView.as_view(),
         name='list-subject-specific-view-course-contents'),
    path('<int:pk>/delete-subject-course-content',
         views.InstituteDeleteSubjectCourseContentView.as_view(),
         name='delete-subject-course-content'),
    path('<slug:subject_slug>/<int:pk>/edit-subject-course-content',
         views.InstituteSubjectEditCourseContentView.as_view(),
         name='edit-subject-course-content'),
    path('<slug:subject_slug>/add-week',
         views.InstituteSubjectViewAddWeekView.as_view(),
         name='add-week'),
    path('<slug:subject_slug>/add-view',
         views.InstituteSubjectAddModuleView.as_view(),
         name='add-view'),
    path('<slug:subject_slug>/<slug:view_key>/edit-subject-view-name',
         views.InstituteEditSubjectModuleViewName.as_view(),
         name='edit-subject-view-name'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:view_key>/<int:week_value>/delete-week',
         views.InstituteSubjectDeleteWeekView.as_view(),
         name='delete-week'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:view_key>/delete-subject-view',
         views.InstituteSubjectDeleteModuleView.as_view(),
         name='delete-subject-view'),
    # Institute Subject preview course
    path('<slug:institute_slug>/<slug:subject_slug>/subject-course-preview-min-details',
         views.InstituteSubjectCoursePreviewMinDetails.as_view(),
         name='subject-course-preview-min-details'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:view_key>/preview-subject-specific-view-contents',
         views.PreviewInstituteSubjectSpecificViewContents.as_view(),
         name='preview-subject-specific-view-contents'),
    path('<slug:institute_slug>/<slug:subject_slug>/<int:course_content_id>/ask-new-question',
         views.InstituteSubjectCourseContentAskQuestionView.as_view(),
         name='ask-new-question'),
    # Institute section
    path('<slug:class_slug>/create-section',
         views.CreateSectionView.as_view(),
         name='create-section'),
    path('<slug:class_slug>/list-all-section',
         views.ListAllSectionView.as_view(),
         name='list-all-section'),
    path('add-section-permission',
         views.AddSectionPermissionView.as_view(),
         name='add-section-permission'),
    path('<slug:section_slug>/list-section-incharges',
         views.ListSectionInchargesView.as_view(),
         name='list-section-incharges'),
]
