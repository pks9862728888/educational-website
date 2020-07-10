from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView,\
    RetrieveAPIView
from rest_framework.response import Response
from django.utils.translation import ugettext as _

from . import serializer

from core.models import Institute, InstituteAdmin, InstituteStaff,\
    InstituteFaculty


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


class CreateInstituteView(CreateAPIView):
    """View for creating institute by teacher"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = serializer.CreateInstituteSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class_ = self.get_serializer_class()
        context = self.get_serializer_context()
        context['user'] = self.request.user
        kwargs['context'] = context
        return serializer_class_(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Overriding create method to send only slug field
        and created status
        """
        serializer_ = self.get_serializer(data=request.data)
        serializer_.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer_)
            headers = self.get_success_headers(serializer_.data)
            return Response({
                'created': 'true',
                'url': serializer_.data['url']
            }, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response({
                'created': 'false',
                'message': _('You have already created an institute with this name.')
            }, status=status.HTTP_400_BAD_REQUEST)


class InstituteFullDetailsView(RetrieveAPIView):
    """View for getting full details of the institute"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = serializer.InstituteFullDetailsSerializer
    queryset = Institute.objects.all()
    lookup_field = 'institute_slug'


class InstituteAdminAddView(APIView):
    """View for adding admin permission"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = serializer.InstituteAdminAddSerializer

    def post(self, request, *args, **kwargs):
        """
        Only active admin can appoint admin.
        Admin has to be a teacher and can not have other permissions.
        """
        # Ensuring only teacher user can be invited as admin
        invitee = get_user_model().objects.filter(
            email=request.data.get('invitee').strip().lower()).first()

        if not invitee or not invitee.is_teacher:
            return Response({
                'error': _('No teacher user with this email found.')
            }, status=status.HTTP_400_BAD_REQUEST)

        # Checking whether the institute is valid
        institute = Institute.objects.filter(
            institute_slug=kwargs.get('institute_slug')).first()

        if not institute:
            return Response({
                'error': _('Institute not found.')
            }, status=status.HTTP_400_BAD_REQUEST)

        # Checking whether the inviter is admin
        inviter_admin = InstituteAdmin.objects.filter(
            invitee=self.request.user,
            institute=institute,
            active=True
        ).first()

        if not inviter_admin:
            return Response({
                'error': _('Only active institute admin can add other admin.')
            }, status=status.HTTP_403_FORBIDDEN)

        # Ensuring user can be invited only once
        already_invited = InstituteAdmin.objects.filter(
            invitee=invitee,
            institute=institute
        ).first()

        if already_invited:
            return Response({
                'error': _('Invitation already sent.')
            }, status=status.HTTP_400_BAD_REQUEST)

        staff_permissions = InstituteStaff.objects.filter(
            institute=institute,
            invitee=invitee
        ).first()

        if staff_permissions:
            if staff_permissions.active:
                return Response({
                    'error': _('Revoke staff permission and try again.')
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error': _('Delete staff invitation and try again.')
                }, status=status.HTTP_400_BAD_REQUEST)

        faculty_permissions = InstituteFaculty.objects.filter(
            institute=institute,
            invitee=invitee
        ).first()

        if faculty_permissions:
            if faculty_permissions.active:
                return Response({
                    'error': _('Revoke faculty permission and try again.')
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error': _('Delete faculty invitation and try again.')
                }, status=status.HTTP_400_BAD_REQUEST)

        ser = self.serializer_class(data={
            'inviter': self.request.user.pk,
            'invitee': invitee.pk,
            'institute': institute.pk
        })
        if ser.is_valid():
            try:
                ser.save()
                return Response({'requested': 'True'}, status=status.HTTP_200_OK)
            except:
                return Response(
                    {'message': _('Internal server error. Please report it to Eduweb.')},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(ser.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class InstituteStaffAddView(APIView):
    """View for adding staff"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher,)
    serializer_class = serializer.InstituteStaffAddSerializer

    def post(self, request, *args, **kwargs):
        """
        Only active admin can appoint staff.
        Staff has to be a teacher and can not have other permissions.
        """
        institute = Institute.objects.filter(
            institute_slug=kwargs.get('institute_slug')
        ).first()

        if not institute:
            return Response({'error': 'Invalid institute'},
                            status=status.HTTP_400_BAD_REQUEST)

        invitee = get_user_model().objects.filter(
            email=request.data.get('invitee').strip().lower()
        ).first()

        if not invitee:
            return Response({'error': 'This user does not exist. Correct the email and try again.'},
                            status=status.HTTP_400_BAD_REQUEST)

        admin_permissions = InstituteAdmin.objects.filter(
                institute=institute, invitee=invitee).first()

        if admin_permissions:
            if admin_permissions.active:
                return Response({'error': 'User already has admin permissions.'},
                                status=status.HTTP_400_BAD_REQUEST)

            if not admin_permissions.active:
                return Response({'error': 'Revoke user admin invitation and try again.'},
                                status=status.HTTP_400_BAD_REQUEST)

        faculty_permissions = InstituteFaculty.objects.filter(
            institute=institute, invitee=invitee).first()

        if faculty_permissions:
            if faculty_permissions.active:
                return Response({'error': 'Remove faculty permission and try again.'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Remove faculty invitation and try again.'},
                                status=status.HTTP_400_BAD_REQUEST)

        inviter_is_active_admin = InstituteAdmin.objects.filter(
            institute=institute,
            invitee=self.request.user,
            active=True
        ).exists()

        if not inviter_is_active_admin:
            return Response({'error': 'Insufficient permission.'},
                            status=status.HTTP_400_BAD_REQUEST)

        staff_permission = InstituteStaff.objects.filter(
            institute=institute,
            invitee=invitee
        ).first()

        if staff_permission:
            if staff_permission.active:
                return Response({'error': 'User is already a staff.'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'User is already invited.'},
                                status=status.HTTP_400_BAD_REQUEST)

        ser = self.serializer_class(data={
            'institute': institute.pk,
            'inviter': self.request.user.pk,
            'invitee': invitee.pk
        })

        if ser.is_valid():
            try:
                ser.save()
                return Response(
                    {'status': 'INVITED'}, status=status.HTTP_200_OK)
            except:
                return Response(
                    {'error': 'Internal error occurred. Kindly contact EduWeb.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class InstituteAdminAcceptDeclineView(APIView):
    """View for accepting or declining admin request"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsTeacher, )

    def post(self, request, *args, **kwargs):
        """For performing operations"""
        operation_type = request.data.get('operation')
        delete_request_by_inviter = request.data.get('invitee')
        institute = Institute.objects.filter(
            institute_slug=kwargs['institute_slug']
        ).first()

        if not institute:
            return Response(
                {'error': _('Institute not found.')},
                status=status.HTTP_400_BAD_REQUEST)

        if operation_type == 'ACCEPT':
            invitee = self.request.user
            invitation = InstituteAdmin.objects.filter(
                institute=institute,
                invitee=invitee
            ).first()

            if not invitation:
                return Response(
                    {'error': _('Invitation may have been deleted' +
                                ' or you are unauthorized to' +
                                ' perform this action.')},
                    status=status.HTTP_400_BAD_REQUEST)

            if invitation.active:
                return Response(
                    {'error': _('Invitation already accepted.')},
                    status=status.HTTP_400_BAD_REQUEST)

            try:
                invitation.active = True
                invitation.request_accepted_on = timezone.now()
                invitation.save()
                return Response(
                    {'status': _('ACCEPTED')},
                    status=status.HTTP_200_OK)
            except:
                return Response(
                    {'error': _('Internal server error. Please contact Eduweb.')},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif operation_type == 'DELETE':
            # Invitee is trying to decline the admin request
            if not delete_request_by_inviter:
                invitee = self.request.user
                invitation = InstituteAdmin.objects.filter(
                    institute=institute,
                    invitee=invitee
                )

                if not invitation:
                    return Response(
                        {'error': _('Invitation may have been deleted already.')},
                        status=status.HTTP_400_BAD_REQUEST)

                if invitee == institute.user:
                    return Response(
                        {'error': _('Owner can\'t remove self admin role' +
                                    ' without appointing another owner.')},
                        status=status.HTTP_400_BAD_REQUEST)

                # Deleting the request
                invitation.delete()
                return Response(
                    {'status': _('DELETED')},
                    status=status.HTTP_200_OK)

            # Admin is trying to decline the request
            elif delete_request_by_inviter:
                invitee_email = request.data.get('invitee')
                invitee = get_user_model().objects.filter(
                    email=invitee_email)

                if not invitee:
                    return Response(
                        {'error': _('This user does not exist.')},
                        status=status.HTTP_400_BAD_REQUEST)

                inviter = InstituteAdmin.objects.filter(
                    inviter=self.request.user,
                    active=True,
                    institute=institute
                )

                if not inviter.exists():
                    return Response(
                        {'error': _('You don\'t have permission to delete the request.')},
                        status=status.HTTP_400_BAD_REQUEST)

                invitation = InstituteAdmin.objects.filter(
                    institute=institute,
                    invitee=invitee.first()
                )

                if not invitation:
                    return Response(
                        {'error': _('Invitation may have been deleted already.')},
                        status=status.HTTP_400_BAD_REQUEST)

                invitation.delete()
                return Response(
                    {'status': _('DELETED')},
                    status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid operation'},
                status=status.HTTP_400_BAD_REQUEST)


class InstituteStaffAcceptDeclineView(APIView):
    """View for accepting and deleting staff permission"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsTeacher, )

    def post(self, request, *args, **kwargs):
        """For handling post request"""
        institute = Institute.objects.filter(
            institute_slug=kwargs.get('institute_slug')).first()

        if not institute:
            return Response(
                {'error': 'Institute not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get('operation') == 'ACCEPT':
            invitation = InstituteStaff.objects.filter(
                institute=institute,
                invitee=self.request.user
            ).first()

            if not invitation:
                return Response(
                    {'error': 'Invitation deleted or unauthorized.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if invitation.active:
                return Response(
                    {'error': 'Staff role request already accepted.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                invitation.active = True
                invitation.request_accepted_on = timezone.now()
                invitation.save()
                return Response(
                    {'status': _('ACCEPTED')},
                    status=status.HTTP_200_OK)
            except:
                return Response(
                    {'error': _('Internal server error. Please contact Eduweb.')},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif request.data.get('operation') == 'DELETE':
            if request.data.get('invitee'):
                requester = self.request.user
                requester_is_admin = InstituteAdmin.objects.filter(
                    institute=institute,
                    invitee=requester,
                    active=True
                ).exists()

                if not requester_is_admin:
                    return Response(
                        {'error': _('Insufficient permission.')},
                        status=status.HTTP_400_BAD_REQUEST)

                invitee_email = request.data.get('invitee')
                invitee = get_user_model().objects.filter(
                    email=invitee_email
                ).first()

                if not invitee:
                    return Response(
                        {'error': _('This user does not exist.')},
                        status=status.HTTP_400_BAD_REQUEST)

                invitation = InstituteStaff.objects.filter(
                    institute=institute,
                    invitee=invitee
                ).first()

                if not invitation:
                    return Response(
                        {'error': _('Invitation may have been deleted.')},
                        status=status.HTTP_400_BAD_REQUEST)

                try:
                    invitation.delete()
                    return Response(
                        {'status': 'DELETED'},
                        status=status.HTTP_200_OK
                    )
                except:
                    return Response(
                        {'error': _('Internal server error. Please contact Eduweb.')},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                invitee = self.request.user

                invitation = InstituteStaff.objects.filter(
                    institute=institute,
                    invitee=invitee
                ).first()

                if not invitation:
                    return Response(
                        {'error': _('Invitation deleted or not authorized.')},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                try:
                    invitation.delete()
                    return Response(
                        {'status': _('DELETED')},
                        status=status.HTTP_200_OK)
                except:
                    return Response(
                        {'error': _('Internal server error. Please contact Eduweb.')},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(
                {'error': 'Invalid operation'},
                status=status.HTTP_400_BAD_REQUEST)


class InstituteFacultyAcceptDeclineView(APIView):
    """View for accepting or deleting faculty request"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsTeacher, )

    def post(self, request, *args, **kwargs):
        """For handling post request"""
        institute = Institute.objects.filter(
            institute_slug=kwargs.get('institute_slug')).first()

        if not institute:
            return Response(
                {'error': 'Institute not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get('operation') == 'ACCEPT':
            invitation = InstituteFaculty.objects.filter(
                institute=institute,
                invitee=self.request.user
            ).first()

            if not invitation:
                return Response(
                    {'error': 'Invitation deleted or insufficient permission to accept.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if invitation.active:
                return Response(
                    {'error': 'Faculty role request already accepted.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                invitation.active = True
                invitation.request_accepted_on = timezone.now()
                invitation.save()
                return Response(
                    {'status': _('ACCEPTED')},
                    status=status.HTTP_200_OK)
            except:
                return Response(
                    {'error': _('Internal server error. Please contact Eduweb.')},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.data.get('operation') == 'DELETE':
            if request.data.get('invitee'):
                requester = self.request.user
                requester_is_admin = InstituteAdmin.objects.filter(
                    institute=institute,
                    invitee=requester,
                    active=True
                ).exists()

                if not requester_is_admin:
                    return Response(
                        {'error': _('Insufficient permission.')},
                        status=status.HTTP_400_BAD_REQUEST)

                invitee_email = request.data.get('invitee')
                invitee = get_user_model().objects.filter(
                    email=invitee_email
                ).first()

                if not invitee:
                    return Response(
                        {'error': _('This user does not exist.')},
                        status=status.HTTP_400_BAD_REQUEST)

                invitation = InstituteFaculty.objects.filter(
                    institute=institute,
                    invitee=invitee
                ).first()

                if not invitation:
                    return Response(
                        {'error': _('Invitation may have been deleted.')},
                        status=status.HTTP_400_BAD_REQUEST)

                try:
                    invitation.delete()
                    return Response(
                        {'status': 'DELETED'},
                        status=status.HTTP_200_OK
                    )
                except:
                    return Response(
                        {'error': _('Internal server error. Please contact Eduweb.')},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                invitee = self.request.user

                invitation = InstituteFaculty.objects.filter(
                    institute=institute,
                    invitee=invitee
                ).first()

                if not invitation:
                    return Response(
                        {'error': _('Invitation deleted or not authorized.')},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                try:
                    invitation.delete()
                    return Response(
                        {'status': _('DELETED')},
                        status=status.HTTP_200_OK)
                except:
                    return Response(
                        {'error': _('Internal server error. Please contact Eduweb.')},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(
                {'error': 'Invalid operation'},
                status=status.HTTP_400_BAD_REQUEST)
