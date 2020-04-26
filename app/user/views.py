# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializer import CreateUserSerializer, LoginUserSerializer


class CreateUserView(generics.CreateAPIView):
    """Creates a new user in system"""
    serializer_class = CreateUserSerializer


class LoginUserView(ObtainAuthToken):
    """Validates login credentials & returns token, username & permissions"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email,
            'username': user.username,
            'is_teacher': user.is_teacher,
            'is_student': user.is_student,
            'is_staff': user.is_staff,
            'is_active': user.is_active
        })
