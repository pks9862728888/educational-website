from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.generics import ListAPIView

from . import serializer

from core.models import Institute


class IsTeacher(permissions.BasePermission):
    """Permission that allows only teacher to access this view"""

    def has_permission(self, request, view):
        """
        Return `True` if teacher is user, `False` otherwise.
        """
        if request.user and request.user.is_teacher:
            return True
        else:
            return False


class InstituteMinDetailsTeacherView(ListAPIView):
    """
    View for getting the min details of institute
    by admin teacher"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = serializer.InstituteMinDetailsSerializer
    queryset = Institute.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
