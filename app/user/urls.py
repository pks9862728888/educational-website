from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('signup', views.CreateUserView.as_view(), name='user-signup'),
    path('login', views.LoginUserView.as_view(), name="user-login")
]
