from django.urls import path

from . import views

app_name = 'teacher'

urlpatterns = [
    path(
        'teacher-profile',
        views.ManageTeacherProfileView.as_view(),
        name='teacher-profile'),
    path(
        'create-classroom',
        views.CreateClassroomView.as_view(),
        name='create-classroom'),
    path(
        'create-subject',
        views.CreateSubjectView.as_view(),
        name='create-subject'),
]
