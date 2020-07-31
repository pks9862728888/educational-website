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
    path('<slug:institute_slug>/list-all-class',
         views.ListAllClassView.as_view(),
         name='list-all-class')
]
