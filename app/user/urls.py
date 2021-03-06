from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'user'

urlpatterns = [
    path('signup', views.CreateUserView.as_view(), name='user-signup'),
    path('login', views.LoginUserView.as_view(), name="user-login"),
    path(
        'user-profile',
        views.ManageUserProfileView.as_view(),
        name='user-profile'),
    path(
        'list-profile-picture',
        views.ListProfilePictureView.as_view(),
        name='list-profile-picture'
    ),
    path(
        'upload-profile-picture',
        views.UploadProfilePictureView.as_view(),
        name="upload-profile-picture"
    ),
    path(
        'set-profile-picture',
        views.SetDeleteProfilePictureView.as_view(),
        name="set-profile-picture"
    ),
    path(
        'delete-profile-picture/<int:pk>',
        views.SetDeleteProfilePictureView.as_view(),
        name="delete-profile-picture"
    ),
    path(
        'remove-class-profile-picture',
        views.RemoveClassProfilePictureView.as_view(),
        name="remove-class-profile-picture"
    ),
    path(
        'remove-public-profile-picture',
        views.RemovePublicProfilePictureView.as_view(),
        name="remove-public-profile-picture"
    ),
    path(
        'user-profile-picture-count',
        views.ProfilePictureCountView.as_view(),
        name="user-profile-picture-count"
    ),
    path(
        'check-profile-data-exists',
        views.CheckProfileDataExists.as_view(),
        name="check-profile-data-exists"
    ),
    path('get-auth-token', obtain_auth_token, name='get-auth-token')
]
