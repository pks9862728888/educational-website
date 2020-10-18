from django.urls import path

from . import views

app_name = 'institute'

urlpatterns = [
    # Institute license related url
    path('get-discount-coupon',
         views.GetInstituteDiscountCouponView.as_view(),
         name='get-discount-coupon'),
    path('<slug:institute_slug>/<slug:product_type>/get-ordered-license-orders',
         views.InstituteOrderedLicenseOrderDetailsView.as_view(),
         name='get-ordered-license-orders'),
    path('<slug:institute_slug>/license-exists-statistics',
         views.InstituteMinLicenseStatisticsView.as_view(),
         name='license-exists-statistics'),

    # For storage license
    path('<slug:institute_slug>/institute-storage-license-cost',
         views.InstituteLicenseCostView.as_view(),
         name="institute-storage-license-cost"),
    path('<slug:institute_slug>/create-storage-license-order',
         views.InstituteCreateStorageLicenseOrderView.as_view(),
         name='create-storage-license-order'),
    path('razorpay-storage-payment-callback',
         views.RazorpayStoragePaymentCallbackView.as_view(),
         name='razorpay-storage-payment-callback'),
    path('<slug:institute_slug>/<int:license_order_id>/delete-unpaid-storage-license',
         views.DeleteUnpaidStorageLicenseView.as_view(),
         name='delete-unpaid-storage-license'),
    path('<slug:institute_slug>/<int:license_order_id>/storage-license-credentials-for-retry-payment',
         views.StorageLicenseCredentialsForRetryPaymentView.as_view(),
         name='storage-license-credentials-for-retry-payment'),

    # For common license
    path('institute-common-license-list',
         views.InstituteCommonLicenseListView.as_view(),
         name="institute-common-license-list"),
    path('<slug:institute_slug>/institute-common-license-detail',
         views.InstituteCommonLicenseDetailView.as_view(),
         name="institute-common-license-detail"),
    path('select-common-license',
         views.InstituteSelectCommonLicenseView.as_view(),
         name='select-common-license'),
    path('create-common-license-order',
         views.InstituteCreateCommonLicenseOrderView.as_view(),
         name='create-common-license-order'),
    path('razorpay-common-license-payment-callback',
         views.RazorpayCommonLicensePaymentCallbackView.as_view(),
         name='razorpay-common-license-payment-callback'),
    path('razorpay-webhook-callback',
         views.RazorpayWebhookCallbackView.as_view(),
         name='razorpay-webhook-callback'),
    path('<slug:institute_slug>/<int:selected_license_id>/get-selected-common-license-details',
         views.InstituteSelectedCommonLicenseDetailsView.as_view(),
         name='get-selected-common-license-details'),
    path('<slug:institute_slug>/<int:license_order_id>/delete-unpaid-common-license',
         views.DeleteUnpaidCommonLicenseView.as_view(),
         name='delete-unpaid-common-license'),
    path('<slug:institute_slug>/<int:license_order_id>/common-license-credentials-for-retry-payment',
         views.CommonLicenseCredentialsForRetryPaymentView.as_view(),
         name='common-license-credentials-for-retry-payment'),

    # Institute related url
    path('create',
         views.CreateInstituteView.as_view(),
         name="create"),
    path('detail/<slug:institute_slug>',
         views.InstituteFullDetailsView.as_view(),
         name="detail"),
    path('institute-min-details-teacher-admin',
         views.InstituteMinDetailsTeacherView.as_view(),
         name="institute-min-details-teacher-admin"),
    path('joined-institutes-teacher',
         views.InstituteJoinedMinDetailsTeacherView.as_view(),
         name="joined-institutes-teacher"),
    path('pending-institute-invites-teacher',
         views.InstitutePendingInviteMinDetailsTeacherView.as_view(),
         name="pending-institute-invites-teacher"),
    path('institute-min-details-student',
         views.InstituteMinDetailsStudentView.as_view(),
         name="institute-min-details-student"),

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
    path('<slug:institute_slug>/add-student-to-institute',
         views.AddStudentToInstituteView.as_view(),
         name="add-student-to-institute"),
    path('<slug:institute_slug>/institute-student-list/<slug:student_type>',
         views.InstituteStudentListView.as_view(),
         name="institute-student-list"),
    path('<slug:institute_slug>/edit-institute-student-details',
         views.EditInstituteStudentDetailsView.as_view(),
         name="edit-institute-student-details"),
    path('<slug:institute_slug>/get-institute-student-user-profile-details',
         views.GetUserProfileDetailsOfInstituteView.as_view(),
         name="get-institute-student-user-profile-details"),
    path('<slug:institute_slug>/join-institute-student',
         views.StudentJoinInstituteView.as_view(),
         name="join-institute-student"),

    # Institute class
    path('<slug:institute_slug>/create-class',
         views.CreateClassView.as_view(),
         name='create-class'),
    path('<slug:class_slug>/delete-class',
         views.DeleteClassView.as_view(),
         name='delete-class'),
    path('<slug:institute_slug>/get-class-slug-name-pairs',
         views.ListSlugNamePairsView.as_view(),
         name="get-class-slug-name-pairs"),
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

    # Institute Class Student
    path('<slug:institute_slug>/<slug:class_slug>/class-student-list/<slug:student_type>',
         views.InstituteClassStudentListView.as_view(),
         name="class-student-list"),
    path('<slug:institute_slug>/<slug:class_slug>/add-student-to-class',
         views.AddStudentToClassView.as_view(),
         name="add-student-to-class"),

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
    # Institute Subject Student
    path('<slug:institute_slug>/<slug:class_slug>/<slug:subject_slug>/subject-student-list/<slug:student_type>',
         views.InstituteSubjectStudentListView.as_view(),
         name="subject-student-list"),
    path('<slug:institute_slug>/<slug:class_slug>/<slug:subject_slug>/add-student-to-subject',
         views.AddStudentToSubjectView.as_view(),
         name="add-student-to-subject"),

    # Institute subject create course
    path('<slug:subject_slug>/add-view',
         views.InstituteSubjectAddModuleView.as_view(),
         name='add-view'),
    path('<slug:subject_slug>/<slug:view_key>/edit-subject-view-name',
         views.InstituteEditSubjectModuleViewName.as_view(),
         name='edit-subject-view-name'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:view_key>/delete-subject-view',
         views.InstituteSubjectDeleteModuleView.as_view(),
         name='delete-subject-view'),
    path('<slug:subject_slug>/subject-course-content-min-statistics',
         views.InstituteSubjectMinStatisticsView.as_view(),
         name='subject-course-content-min-statistics'),
    path('<slug:subject_slug>/<slug:view_key>/list-subject-specific-view-course-contents',
         views.InstituteSubjectSpecificViewCourseContentView.as_view(),
         name='list-subject-specific-view-course-contents'),
    path('<slug:subject_slug>/<int:lecture_id>/list-subject-lecture-contents',
         views.InstituteSubjectLectureContents.as_view(),
         name='list-subject-lecture-contents'),
    path('<slug:subject_slug>/add-subject-lecture',
         views.InstituteSubjectAddLectureView.as_view(),
         name='add-subject-lecture'),
    path('<slug:subject_slug>/<int:lecture_id>/edit-subject-lecture',
         views.InstituteSubjectEditLectureView.as_view(),
         name='edit-subject-lecture'),
    path('<slug:subject_slug>/<int:lecture_id>/delete-subject-lecture',
         views.InstituteSubjectDeleteLectureView.as_view(),
         name='delete-subject-lecture'),
    path('<slug:subject_slug>/add-subject-introductory-content',
         views.InstituteSubjectAddIntroductoryContentView.as_view(),
         name='add-subject-introductory-content'),
    path('<slug:subject_slug>/<int:content_id>/edit-subject-introductory-content',
         views.InstituteSubjectEditIntroductoryContentView.as_view(),
         name='edit-subject-introductory-content'),
    path('<slug:subject_slug>/<int:content_id>/delete-subject-introductory-content',
         views.InstituteSubjectDeleteIntroductoryContentView.as_view(),
         name='delete-subject-introductory-content'),
    path('<slug:subject_slug>/<int:lecture_id>/add-lecture-materials',
         views.InstituteSubjectAddLectureMaterials.as_view(),
         name='add-lecture-materials'),
    path('<slug:subject_slug>/<int:lecture_material_id>/edit-lecture-material',
         views.InstituteSubjectEditLectureMaterial.as_view(),
         name='edit-lecture-material'),
    path('<slug:subject_slug>/<int:lecture_material_id>/delete-lecture-material',
         views.InstituteSubjectDeleteLectureMaterial.as_view(),
         name='delete-lecture-material'),
    path('<slug:subject_slug>/<int:lecture_id>/add-lecture-use-case-or-additional-reading-link',
         views.InstituteAddLectureUseCaseOrAdditionalReading.as_view(),
         name='add-lecture-use-case-or-additional-reading-link'),
    path('<slug:subject_slug>/<int:content_id>/edit-lecture-use-case-or-additional-reading-link',
         views.InstituteEditLectureUseCaseOrAdditionalReading.as_view(),
         name='edit-lecture-use-case-or-additional-reading-link'),
    path('<slug:subject_slug>/<int:content_id>/delete-lecture-use-case-or-additional-reading-link',
         views.InstituteDeleteLectureUseCaseOrAdditionalReading.as_view(),
         name='delete-lecture-use-case-or-additional-reading-link'),
    path('<slug:subject_slug>/<int:lecture_id>/add-lecture-objective-or-use-case-text',
         views.InstituteAddLectureObjectiveOrUseCaseText.as_view(),
         name='add-lecture-objective-or-use-case-text'),
    path('<slug:subject_slug>/<int:content_id>/edit-lecture-objective-or-use-case-text',
         views.InstituteEditLectureObjectiveOrUseCaseText.as_view(),
         name='edit-lecture-objective-or-use-case-text'),
    path('<slug:subject_slug>/<int:content_id>/delete-lecture-objective-or-use-case-text',
         views.InstituteDeleteLectureObjectiveOrUseCaseText.as_view(),
         name='delete-lecture-objective-or-use-case-text'),

    # Institute Add Test
    path('<slug:institute_slug>/<slug:subject_slug>/add-test',
         views.InstituteSubjectAddTestView.as_view(),
         name='institute-subject-add-test'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:test_slug>/get-test-min-details',
         views.InstituteTestMinDetailsView.as_view(),
         name='get-test-min-details'),
    path('<slug:subject_slug>/<slug:test_slug>/get-test-details-for-question-paper-creation',
         views.InstituteTestMinDetailsForQuestionCreationView.as_view(),
         name='get-test-details-for-question-paper-creation'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:test_slug>/<int:set_id>/get-question-set-questions',
         views.InstituteGetQuestionSetQuestionsView.as_view(),
         name='get-question-set-questions'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:test_slug>/add-question-set',
         views.InstituteAddQuestionSetView.as_view(),
         name='add-question-set'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:test_slug>/<int:set_id>/delete-test-set',
         views.InstituteDeleteTestSetView.as_view(),
         name='delete-test-set'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:test_slug>/add-test-concept-label',
         views.InstituteAddTestConceptLabelView.as_view(),
         name='add-test-concept-label'),
    path('<slug:institute_slug>/<slug:subject_slug>/<int:label_id>/delete-test-concept-label',
         views.InstituteDeleteTestConceptLabelView.as_view(),
         name='delete-test-concept-label'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:test_slug>/<int:set_id>/add-test-question-section',
         views.InstituteAddTestQuestionSectionView.as_view(),
         name='add-test-question-section'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:test_slug>/<int:set_id>/edit-question-set-name',
         views.InstituteEditQuestionSetName.as_view(),
         name='edit-question-set-name'),

    # File question paper
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:test_slug>/<int:set_id>/upload-file-question-paper',
         views.InstituteUploadFileQuestionPaperView.as_view(),
         name='upload-file-question-paper'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:test_slug>/<int:set_id>/delete-file-question-paper',
         views.InstituteDeleteFileQuestionPaperView.as_view(),
         name='delete-file-question-paper'),

    # Image question paper
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:test_slug>/<int:set_id>/<int:test_section_id>/upload-image'
         '-test-question',
         views.InstituteUploadImageQuestionView.as_view(),
         name='upload-image-test-question'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:test_slug>/<int:set_id>/<int:question_id>/edit-image'
         '-test-question',
         views.InstituteEditImageQuestionView.as_view(),
         name='edit-image-test-question'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:test_slug>/<int:set_id>/<int:question_id>/delete-image'
         '-test-question',
         views.InstituteDeleteImageQuestionView.as_view(),
         name='delete-image-test-question'),

    # Institute Subject preview course
    path('list-all-student-institute-courses',
         views.InstituteStudentCourseListView.as_view(),
         name='list-all-student-institute-courses'),
    path('bookmark-course',
         views.BookmarkInstituteCourse.as_view(),
         name='bookmark_course'),
    path('<slug:institute_slug>/<slug:subject_slug>/list-subject-peers',
         views.ListSubjectPeers.as_view(),
         name='list-subject-peers'),
    path('<slug:institute_slug>/<slug:subject_slug>/subject-course-preview-min-details',
         views.InstituteSubjectCoursePreviewMinDetails.as_view(),
         name='subject-course-preview-min-details'),
    path('<slug:institute_slug>/<slug:subject_slug>/<slug:view_key>/preview-subject-specific-view-contents',
         views.PreviewInstituteSubjectSpecificViewContents.as_view(),
         name='preview-subject-specific-view-contents'),
    path('<slug:institute_slug>/<slug:subject_slug>/<int:course_content_id>/ask-new-question',
         views.InstituteSubjectCourseContentAskQuestionView.as_view(),
         name='ask-new-question'),
    path('<slug:institute_slug>/<slug:subject_slug>/<int:question_pk>/answer-question',
         views.InstituteSubjectCourseContentAnswerQuestionView.as_view(),
         name='answer-question'),
    path('<slug:institute_slug>/<slug:subject_slug>/<int:question_pk>/upvote-downvote-question',
         views.InstituteSubjectUpvoteDownvoteQuestionView.as_view(),
         name='upvote-downvote-question'),
    path('<slug:institute_slug>/<slug:subject_slug>/<int:answer_pk>/upvote-downvote-answer',
         views.InstituteSubjectUpvoteDownvoteAnswerView.as_view(),
         name='upvote-downvote-answer'),
    path('<int:question_pk>/delete-question',
         views.InstituteSubjectCourseContentDeleteQuestionView.as_view(),
         name='delete-question'),
    path('<slug:subject_slug>/<int:answer_pk>/delete-answer',
         views.InstituteSubjectCourseContentDeleteAnswerView.as_view(),
         name='delete-answer'),
    path('<slug:institute_slug>/<slug:subject_slug>/<int:question_pk>/edit-question',
         views.InstituteSubjectCourseContentEditQuestionView.as_view(),
         name='edit-question'),
    path('<slug:institute_slug>/<slug:subject_slug>/<int:answer_pk>/edit-answer',
         views.InstituteSubjectCourseContentEditAnswerView.as_view(),
         name='edit-answer'),
    path('<int:answer_pk>/pin-unpin-answer',
         views.InstituteSubjectCourseContentPinUnpinAnswerView.as_view(),
         name='pin-unpin-answer'),
    path('<slug:institute_slug>/<slug:subject_slug>/<int:question_pk>/list-answers',
         views.InstituteSubjectCourseQuestionListAnswerView.as_view(),
         name='list-answers'),
    path('<slug:institute_slug>/<slug:subject_slug>/<int:course_content_pk>/list-questions',
         views.InstituteSubjectCourseListQuestionView.as_view(),
         name='list-questions'),
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
