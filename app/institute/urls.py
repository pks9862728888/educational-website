from django.urls import path

from . import views

app_name = 'institute'

urlpatterns = [
    path('institute-min-details-teacher-admin',
         views.InstituteMinDetailsTeacherView.as_view(),
         name="institute-min-details-teacher-admin"),
    path('create',
         views.CreateInstituteView.as_view(),
         name="create"),
    path('detail/<slug:institute_slug>',
         views.InstituteFullDetailsView.as_view(),
         name="detail"),
    path('<slug:institute_slug>/add-admin',
         views.InstituteAdminAddView.as_view(),
         name="request_for_admin"),
    path('<slug:institute_slug>/add-staff',
         views.InstituteStaffAddView.as_view(),
         name="request_for_staff"),
    path('<slug:institute_slug>/accept-or-delete-admin',
         views.InstituteAdminAcceptDeclineView.as_view(),
         name="accept_delete_admin_request"),
    path('<slug:institute_slug>/accept-or-delete-staff',
         views.InstituteStaffAcceptDeclineView.as_view(),
         name="accept_delete_staff_request"),
    path('<slug:institute_slug>/accept-or-delete-faculty',
         views.InstituteFacultyAcceptDeclineView.as_view(),
         name="accept_delete_faculty_request"),
]
