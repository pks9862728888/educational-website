from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from . import serializer


class ManageTeacherProfileView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = serializer.ManageTeacherProfileSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        """Retrieve and return authenticated user and profile data"""
        return self.request.user

    def get_serializer(self, instance=None, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        return serializer_class(instance, *args, **kwargs,
                                context={"request": self.request})
