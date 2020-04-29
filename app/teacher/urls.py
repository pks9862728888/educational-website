from django.urls import path

from . import views

app_name = 'teacher'

urlpatterns = [
    path(
        'create-subject',
        views.CreateSubjectView.as_view(),
        name='create-subject'),
]
