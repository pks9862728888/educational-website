from django.urls import path

from . import views

app_name = 'teacher'

urlpatterns = [
    path(
        'teacher-profile',
        views.ManageUserProfileView.as_view(),
        name='teacher-profile'),
]
