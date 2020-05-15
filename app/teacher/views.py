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


class CreateClassroomView(APIView):
    """View for creating a new classroom"""
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    serializer_class = serializer.CreateClassroomSerializer

    def post(self, request, *args, **kwargs):
        serializer_ = serializer.CreateClassroomSerializer(
            data=request.data, context={"request": request})
        if serializer_.is_valid():
            serializer_.save()
            return Response(serializer_.data, status=status.HTTP_201_CREATED)

        return Response(serializer_.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateSubjectView(APIView):
    """View for creating a new subject"""
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    serializer_class = serializer.CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer_ = serializer.CreateUserSerializer(
            data=request.data, context={"request": request})
        if serializer_.is_valid():
            serializer_.save()
            return Response(serializer_.data, status=status.HTTP_201_CREATED)

        return Response(serializer_.errors, status=status.HTTP_400_BAD_REQUEST)
