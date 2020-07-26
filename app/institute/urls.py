from django.urls import path

from . import views

app_name = 'institute'

urlpatterns = [
    path('get-discount-coupon',
         views.GetInstituteDiscountCouponView.as_view(),
         name='get-discount-coupon'),
    path('institute-license-list',
         views.InstituteLicenseListView.as_view(),
         name="institute-license-list"),
    path('institute-license-detail',
         views.InstituteLicenseDetailView.as_view(),
         name="institute-license-detail"),
    path('confirm-license-plan',
         views.InstituteConfirmLicensePlan.as_view(),
         name='confirm-license-plan'),
    path('institute-min-details-teacher-admin',
         views.InstituteMinDetailsTeacherView.as_view(),
         name="institute-min-details-teacher-admin"),
    path('joined-institutes-teacher',
         views.InstituteJoinedMinDetailsTeacherView.as_view(),
         name="joined-institutes-teacher"),
    path('pending-institute-invites-teacher',
         views.InstitutePendingInviteMinDetailsTeacherView.as_view(),
         name="pending-institute-invites-teacher"),
    path('create',
         views.CreateInstituteView.as_view(),
         name="create"),
    path('detail/<slug:institute_slug>',
         views.InstituteFullDetailsView.as_view(),
         name="detail"),
    path('<slug:institute_slug>/provide-permission',
         views.InstituteProvidePermissionView.as_view(),
         name="provide_permission"),
    path('<slug:institute_slug>/accept-delete-permission',
         views.InstitutePermissionAcceptDeleteView.as_view(),
         name="accept_delete_permission"),
    path('<slug:institute_slug>/<slug:role>/get-user-list',
         views.InstitutePermittedUserListView.as_view(),
         name="get_permission_list"),
]
