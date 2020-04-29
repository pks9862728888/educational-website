from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView

from . import serializer


class CreateSubjectView(CreateAPIView):
    """View for creating a new subject"""
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    serializer_class = serializer.CreateUserSerializer
