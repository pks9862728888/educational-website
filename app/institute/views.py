import json
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext as _

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView,\
    RetrieveAPIView
from rest_framework.response import Response

from . import serializer

from core.models import Institute, InstituteRole,\
    InstitutePermission, InstituteLicense, Billing,\
    InstituteDiscountCoupon, InstituteSelectedLicense,\
    InstituteLicenseOrderDetails


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


class GetInstituteDiscountCouponView(APIView):
    """View to get institute discount coupon"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        """Used for getting discount coupon details"""
        if not InstitutePermission.objects.filter(
            invitee=self.request.user.pk,
            role=InstituteRole.ADMIN
        ).exists():
            return Response({'error': _('Invalid permission')},
                            status=status.HTTP_400_BAD_REQUEST)

        coupon_code = request.data.get('coupon_code')

        if not coupon_code:
            return Response({'error': _('Coupon code is required.')},
                            status=status.HTTP_400_BAD_REQUEST)

        coupon = InstituteDiscountCoupon.objects.filter(
            coupon_code=coupon_code
        ).first()

        if not coupon:
            return Response({'error': _('Coupon not found.')},
                            status=status.HTTP_400_BAD_REQUEST)
        if not coupon.active:
            return Response({'error': _('Coupon already used.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() > coupon.expiry_date:
            return Response({'error': _('Coupon expired.')},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'discount_rs': coupon.discount_rs,
                         'active': coupon.active},
                        status=status.HTTP_200_OK)


class InstituteLicenseListView(ListAPIView):
    """
    View for getting list of all available institute license
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = serializer.InstituteLicenseListSerializer

    def get(self, *args, **kwargs):
        """Used for formatting and sending structured data"""
        licenses = InstituteLicense.objects.all()
        monthly_license = licenses.filter(
            billing=Billing.MONTHLY).order_by('type')
        yearly_license = licenses.filter(
            billing=Billing.ANNUALLY).order_by('type')

        monthly_license_list = []
        yearly_license_list = []

        for _license in monthly_license:
            ser = self.serializer_class(_license)
            monthly_license_list.append(ser.data)

        for _license in yearly_license:
            ser = self.serializer_class(_license)
            yearly_license_list.append(ser.data)

        return Response({
            'monthly_license': monthly_license_list,
            'yearly_license': yearly_license_list
        }, status=status.HTTP_200_OK)


class InstituteLicenseDetailView(APIView):
    """
    View for getting institute license details
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        try:
            id_ = int(request.data.get('id'))
        except Exception:
            return Response({'id': _('Invalid id.')})

        if not id_:
            return Response({'error': _('Id is required.')})

        if not InstitutePermission.objects.filter(
            invitee=self.request.user.pk,
            role=InstituteRole.ADMIN
        ).exists():
            return Response({'error': 'Unauthorized request.'},
                            status=status.HTTP_400_BAD_REQUEST)

        license_ = InstituteLicense.objects.filter(pk=id_).values()

        if license_:
            return Response(license_[0], status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'License not Found'
            }, status=status.HTTP_400_BAD_REQUEST)


class InstituteConfirmLicensePlan(APIView):
    """View for confirming institute license"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        institute_slug = request.data.get('institute_slug')
        license_id = request.data.get('license_id')
        coupon_code = request.data.get('coupon_code')

        errors = {}
        if not institute_slug:
            errors['institute_slug'] = _('This field is required.')
        if not license_id:
            errors['license_id'] = _('This field is required.')

        if errors:
            return Response(
                errors, status=status.HTTP_400_BAD_REQUEST)

        institute = Institute.objects.filter(
            institute_slug=institute_slug
        ).first()
        if not institute:
            return Response({'error': _('Invalid request.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not InstitutePermission.objects.filter(
            institute=institute.pk,
            invitee=self.request.user.pk,
            active=True,
            role=InstituteRole.ADMIN
        ):
            return Response({'error': _('Insufficient permission')},
                            status=status.HTTP_400_BAD_REQUEST)
        coupon = None
        if coupon_code:
            coupon = InstituteDiscountCoupon.objects.filter(
                coupon_code=coupon_code
            ).first()

            if not coupon.active:
                return Response({'coupon_code': _('Coupon already used.')},
                                status=status.HTTP_400_BAD_REQUEST)
            if timezone.now() > coupon.expiry_date:
                return Response({'coupon_code': _('Coupon expired.')},
                                status=status.HTTP_400_BAD_REQUEST)

        license_ = InstituteLicense.objects.filter(
            pk=license_id
        ).first()
        if not license_:
            return Response({'error': _('License not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            sel_lic = InstituteSelectedLicense.objects.create(
                institute=institute,
                type=license_.type,
                billing=license_.billing,
                amount=license_.amount,
                discount_percent=license_.discount_percent,
                discount_coupon=coupon,
                storage=license_.storage,
                no_of_admin=license_.no_of_admin,
                no_of_staff=license_.no_of_staff,
                no_of_faculty=license_.no_of_faculty,
                no_of_student=license_.no_of_student,
                video_call_max_attendees=license_.video_call_max_attendees,
                classroom_limit=license_.classroom_limit,
                department_limit=license_.department_limit,
                subject_limit=license_.subject_limit,
                scheduled_test=license_.scheduled_test,
                LMS_exists=license_.LMS_exists,
                discussion_forum=license_.discussion_forum
            )
            if sel_lic:
                InstituteLicenseOrderDetails.objects.create(
                    institute=institute,
                    selected_license=sel_lic)
                return Response({'status': _('SUCCESS'),
                                 'net_amount': sel_lic.net_amount},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': _('Internal server error.')},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': _('Internal server error.')},
                            status=status.HTTP_400_BAD_REQUEST)


class InstituteMinDetailsTeacherView(ListAPIView):
    """
    View for getting the min details of institute
    by admin teacher
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = serializer.InstituteMinDetailsSerializer
    queryset = Institute.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        context['user'] = self.request.user
        kwargs['context'] = context
        return serializer_class(*args, **kwargs)


class InstituteJoinedMinDetailsTeacherView(ListAPIView):
    """
    View for getting the min details of joined institutes"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = serializer.InstitutesJoinedMinDetailsTeacher
    queryset = Institute.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            permissions__invitee=self.request.user.pk,
            permissions__active=True).exclude(
            permissions__inviter=self.request.user.pk
        )

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        context['user'] = self.request.user
        kwargs['context'] = context
        return serializer_class(*args, **kwargs)


class InstitutePendingInviteMinDetailsTeacherView(ListAPIView):
    """View for getting the min details of active invites by institutes"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = serializer.InstitutePendingInviteMinDetailsSerializer
    queryset = Institute.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            permissions__invitee=self.request.user.pk,
            permissions__active=False).exclude(
            permissions__inviter=self.request.user.pk
        )

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        context['user'] = self.request.user
        kwargs['context'] = context
        return serializer_class(*args, **kwargs)


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
        except Exception:
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

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        context['user'] = self.request.user
        kwargs['context'] = context
        return serializer_class(*args, **kwargs)


class InstituteProvidePermissionView(APIView):
    """View for providing permission to institute"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = serializer.InstituteProvidePermissionSerializer

    def post(self, request, *args, **kwargs):
        """Method to provide permission on post request"""
        institute = Institute.objects.filter(
            institute_slug=kwargs.get('institute_slug')).first()

        if not institute:
            return Response({'error': _('Invalid institute.')},
                            status=status.HTTP_400_BAD_REQUEST)

        errors = {}
        role = request.data.get('role')
        invitee_email = request.data.get('invitee')
        invitee = None

        if not role:
            errors['role'] = _('This field is required.')
        elif role not in [InstituteRole.STAFF, InstituteRole.FACULTY, InstituteRole.ADMIN]:
            errors['role'] = _('Invalid role.')

        if not invitee_email:
            errors['invitee'] = _('This field is required.')
        else:
            invitee = get_user_model().objects.filter(
                email=invitee_email.lower().strip()).first()
            if not invitee:
                errors['invitee'] = _('This user does not exist.')
            elif not invitee.is_teacher:
                msg = _('Only teacher user can be assigned special roles.')
                errors['invitee'] = msg

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        inviter = self.request.user
        inviter_perm = InstitutePermission.objects.filter(
            institute=institute,
            invitee=inviter,
            active=True
        ).first()

        # For assigning admin or staff role
        if role == InstituteRole.ADMIN or role == InstituteRole.STAFF:
            if not inviter_perm or \
                    inviter_perm.role != InstituteRole.ADMIN:
                return Response({'error': _('Insufficient permission.')},
                                status=status.HTTP_400_BAD_REQUEST)

            existing_invite = InstitutePermission.objects.filter(
                institute=institute,
                invitee=invitee
            ).first()

            if existing_invite and role == InstituteRole.ADMIN:
                if existing_invite.role == InstituteRole.ADMIN and not existing_invite.active:
                    return Response({'invitee': _('User already invited.')},
                                    status=status.HTTP_400_BAD_REQUEST)
                if existing_invite.role == InstituteRole.ADMIN and existing_invite.active:
                    msg = _('User already has admin permission.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == InstituteRole.STAFF:
                    msg = _('Remove staff permission and try again.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == InstituteRole.FACULTY:
                    msg = _('Remove faculty permission and try again.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
            elif existing_invite and role == InstituteRole.STAFF:
                if existing_invite.role == InstituteRole.STAFF and not existing_invite.active:
                    msg = _('User already invited.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == InstituteRole.STAFF and existing_invite.active:
                    msg = _('User already has staff permission.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == InstituteRole.ADMIN and existing_invite.active:
                    msg = _('Unauthorised. User is admin.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == InstituteRole.ADMIN and not existing_invite.active:
                    msg = _('Unauthorised. User was requested to be admin.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == InstituteRole.FACULTY:
                    msg = _('Remove faculty permission and try again.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)

            ser = self.serializer_class(data={
                'inviter': inviter.pk,
                'invitee': invitee.pk,
                'institute': institute.pk,
                'role': role,
            })

            if ser.is_valid():
                try:
                    saved_data = ser.save()
                    response = {
                        'email': str(saved_data.invitee),
                        'image': None,
                        'invitation_id': saved_data.pk,
                        'invitee_id': saved_data.invitee.pk,
                        'inviter': str(self.request.user),
                        'requested_on': saved_data.request_date
                    }
                    return Response(response, status=status.HTTP_200_OK)
                except Exception:
                    msg = _('Internal server error. Please contact Eduweb')
                    return Response({'error': msg},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        # For assigning faculty role
        elif role == InstituteRole.FACULTY:
            if not inviter_perm or \
                    inviter_perm.role == InstituteRole.FACULTY:
                return Response({'error': _('Insufficient permission.')},
                                status=status.HTTP_400_BAD_REQUEST)

            existing_invite = InstitutePermission.objects.filter(
                institute=institute,
                invitee=invitee
            ).first()

            if existing_invite:
                if existing_invite.role == InstituteRole.FACULTY and not existing_invite.active:
                    return Response({'invitee': _('User already invited.')},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == InstituteRole.FACULTY and existing_invite.active:
                    return Response({'invitee': _('User is already a faculty.')},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == InstituteRole.ADMIN and not existing_invite.active:
                    msg = _('Unauthorized. User is already requested for admin role.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == InstituteRole.ADMIN and existing_invite.active:
                    msg = _('Unauthorized. User has admin permissions.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == InstituteRole.STAFF and not existing_invite.active:
                    msg = _('Unauthorized. User is already requested for staff role.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == InstituteRole.STAFF and existing_invite.active:
                    msg = _('Unauthorized. User has staff permissions.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)

            ser = self.serializer_class(data={
                'inviter': inviter.pk,
                'invitee': invitee.pk,
                'institute': institute.pk,
                'role': role,
                'request_accepted_on': timezone.now()
            })

            if ser.is_valid():
                try:
                    saved_data = ser.save()
                    response = {
                        'email': str(saved_data.invitee),
                        'image': None,
                        'invitation_id': saved_data.pk,
                        'invitee_id': saved_data.invitee.pk,
                        'inviter': str(self.request.user),
                        'requested_on': saved_data.request_date
                    }
                    return Response(response, status=status.HTTP_200_OK)
                except Exception:
                    msg = _('Internal server error. Please contact Eduweb')
                    return Response({'error': msg},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class InstitutePermissionAcceptDeleteView(APIView):
    """View for accepting or deleting permission"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        """Method to accept or delete permission on post request"""
        institute = Institute.objects.filter(
            institute_slug=kwargs.get('institute_slug')
        ).first()

        if not institute:
            return Response({'error': _('Invalid institute.')},
                            status=status.HTTP_400_BAD_REQUEST)

        errors = {}
        operation = request.data.get('operation')

        if not operation:
            errors['operation'] = _('This field is required.')
        elif operation.upper() != 'ACCEPT' and operation.upper() != 'DELETE':
            errors['operation'] = _('Invalid operation.')

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if operation.upper() == 'ACCEPT':
            invitee = self.request.user
            invitation = InstitutePermission.objects.filter(
                institute=institute,
                invitee=invitee
            ).first()

            if not invitation:
                return Response({'error': _('Invitation not found or already deleted.')},
                                status=status.HTTP_400_BAD_REQUEST)
            elif invitation.active:
                msg = _('Join request already accepted.')
                return Response({'error': msg},
                                status=status.HTTP_400_BAD_REQUEST)

            invitation.active = True
            invitation.request_accepted_on = timezone.now()
            try:
                invitation.save()
                return Response({'status': 'ACCEPTED'},
                                status=status.HTTP_200_OK)
            except Exception:
                msg = _('Internal server error. Please contact EduWeb.')
                return Response({'error': msg},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif operation.upper() == 'DELETE':
            invitee_email = request.data.get('invitee')

            # Inviter or admin is trying to delete join request
            if invitee_email:
                invitee = get_user_model().objects.filter(
                    email=invitee_email
                ).first()

                if not invitee:
                    msg = _('This user does not exist.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)

                invitation = InstitutePermission.objects.filter(
                    institute=institute,
                    invitee=invitee
                ).first()

                if not invitation:
                    msg = _('Invitation not found or already deleted.')
                    return Response({'error': msg},
                                    status=status.HTTP_400_BAD_REQUEST)

                inviter = InstitutePermission.objects.filter(
                    institute=institute,
                    invitee=self.request.user,
                    active=True
                ).first()

                if not inviter:
                    return Response({'error': 'Permission denied.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                # Active user can not be deleted using this url.
                elif invitation.active and invitation.role != inviter.role:
                    msg = _('Internal server error. Please contact EduWeb.')
                    return Response({'error': msg},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Same role can not delete same role permission
                # Admin can delete staff and faculty permission
                # Staff can only add faculty but not delete
                # Faculty can neither add nor delete
                if inviter.role != InstituteRole.ADMIN or\
                        invitation.active and inviter.role == invitation.role:
                    return Response({'error': _('Permission denied.')},
                                    status=status.HTTP_400_BAD_REQUEST)

                try:
                    invitation.delete()
                    return Response({'status': 'DELETED'},
                                    status=status.HTTP_200_OK)
                except Exception:
                    msg = _('Internal Server Error. Please contact EduWeb.')
                    return Response({'error': msg},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Invitee is trying to delete join request
            else:
                invitation = InstitutePermission.objects.filter(
                    institute=institute,
                    invitee=self.request.user
                ).first()

                if not invitation:
                    msg = _('Invitation not found or already deleted.')
                    return Response({'error': msg},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Deleting invitation
                try:
                    invitation.delete()
                    return Response({'status': 'DELETED'},
                                    status=status.HTTP_200_OK)
                except Exception:
                    msg = _('Internal server error occurred. Please contact EduWeb')
                    return Response({'error': msg},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InstitutePermittedUserListView(APIView):
    """View to get permitted user list"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsTeacher, )

    def _format_data(self, user_invites, active=True):
        """Return list of user details in list"""
        list_user_data = []
        for invite in user_invites:
            user_data = dict()
            user_data['invitation_id'] = invite.pk
            user_data['invitee_id'] = invite.invitee.pk
            user_data['email'] = str(invite.invitee)
            user_data['inviter'] = str(invite.inviter)
            user_data['image'] = None
            if active:
                user_data['request_accepted_on'] = str(invite.request_accepted_on)
            else:
                user_data['requested_on'] = str(invite.request_date)
            list_user_data.append(user_data)
        return list_user_data

    def get(self, *args, **kwargs):
        """Post request to get permitted user of institute"""
        errors = {}
        institute = Institute.objects.filter(
            institute_slug=kwargs.get('institute_slug')
        ).first()
        if not institute:
            errors['institute_slug'] = 'Invalid'

        role = kwargs.get('role').upper()
        if role != 'ADMIN' and role != 'STAFF' and role != 'FACULTY':
            errors['role'] = 'Invalid'

        if errors:
            return Response({'error': _('Invalid credentials.')},
                            status=status.HTTP_400_BAD_REQUEST)

        has_perm = InstitutePermission.objects.filter(
            institute=institute,
            invitee=self.request.user,
            active=True
        ).exists()

        if not has_perm:
            return Response({'error': _('Permission denied.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if role == 'ADMIN':
            permitted_user_invitations = InstitutePermission.objects.filter(
                institute=institute,
                role=InstituteRole.ADMIN
            )
            response_data = {
                'active_admin_list': self._format_data(
                    permitted_user_invitations.filter(active=True)),
                'pending_admin_invites': self._format_data(
                    permitted_user_invitations.filter(active=False), False)
            }
            return Response(response_data, status=status.HTTP_200_OK)
        elif role == 'STAFF':
            permitted_user_invitations = InstitutePermission.objects.filter(
                institute=institute,
                role=InstituteRole.STAFF
            )
            response_data = {
                'active_staff_list': self._format_data(
                    permitted_user_invitations.filter(active=True)),
                'pending_staff_invites': self._format_data(
                    permitted_user_invitations.filter(active=False), False)
            }
            return Response(response_data, status=status.HTTP_200_OK)
        elif role == 'FACULTY':
            permitted_user_invitations = InstitutePermission.objects.filter(
                institute=institute,
                role=InstituteRole.FACULTY
            )
            response_data = {
                'active_faculty_list': self._format_data(
                    permitted_user_invitations.filter(active=True)),
                'pending_faculty_invites': self._format_data(
                    permitted_user_invitations.filter(active=False), False)
            }
            return Response(response_data, status=status.HTTP_200_OK)
