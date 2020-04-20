# from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from . import serializer


class CreateUserView(generics.CreateAPIView):
    """Creates a new user in system"""
    serializer_class = serializer.CreateUserSerializer
