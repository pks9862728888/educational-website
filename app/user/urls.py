from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'user'

urlpatterns = [
    path('signup', views.CreateUserView.as_view(), name='user-signup'),
    path('get-auth-token', obtain_auth_token, name='get-auth-token'),
]
