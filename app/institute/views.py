import os
import sys
import datetime
from decimal import Decimal
import time
import subprocess

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView,\
    RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser

import filetype
from razorpay.errors import SignatureVerificationError
from PIL import Image

import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size, FFProbe

from . import serializer
from app.settings import client, MEDIA_URL, MEDIA_ROOT
from core import models


def get_unexpired_license(institute):
    """
    Returns order if institute has unexpired institute license,
    else returns None
    """
    order = models.InstituteLicenseOrderDetails.objects.filter(
        institute=institute,
        paid=True
    )

    if order.filter(active=True).exists():
        order = order.filter(active=True).first()
    else:
        order = order.order_by('-order_created_on').first()

    if not order or (order.active and order.end_date < timezone.now()):
        return None
    else:
        return order


def get_institute_stats_and_validate(institute, size=None):
    """
    Returns institute statistics if validation success else return error response
    """
    stats = models.InstituteStatistics.objects.filter(institute=institute).first()
    order = get_unexpired_license(institute)
    if not order:
        return Response({'error': _('License not found.')},
                        status=status.HTTP_400_BAD_REQUEST)
    elif size:
        if stats.storage > order.selected_license.storage:
            return Response({'error': _('Maximum storage limit reached. To get more storage contact us.')},
                            status=status.HTTP_400_BAD_REQUEST)
        elif stats.storage + size > order.selected_license.storage:
            return Response({'error': _('File size too large. Allowed storage limit will get exceeded. To get more storage contact us.')},
                            status=status.HTTP_400_BAD_REQUEST)
    return stats


def monitor(ffmpeg, duration, time_, time_left, process):
    """Realtime information about ffmpeg transcoding process"""
    per = round(time_ / duration * 100)
    print('*' * per + str(per) + '% completed')


def get_study_material_content_details(data, data_notation):
    """
    Creates and returns study material data.
    """
    if data_notation == 'SER':
        data.pop('course_content_subject')

        if not data['description']:
            data.pop('description')

        if not data['target_date']:
            data.pop('target_date')

        return data

    elif data_notation == 'OBJ':
        response = dict()
        response['id'] = data.pk
        response['title'] = data.title
        response['order'] = data.order
        response['content_type'] = data.content_type
        response['view'] = data.view
        response['uploaded_on'] = str(data.uploaded_on)

        if data.description:
            response['description'] = data.description

        if data.target_date:
            response['target_date'] = str(data.target_date)

        return response


def get_external_link_study_material_data(data, data_notation):
    """
    Creates and returns external link study material data.
    """
    if data_notation == 'SER':
        return {
            'id': data['id'],
            'url': data['url']
        }
    elif data_notation == 'OBJ':
        return {
            'id': data.pk,
            'url': data.url
        }


def get_image_study_material_data(data, data_notation, base_url, size=None):
    """
    Creates and returns image content data dict,
    size is in GB
    """
    if data_notation == 'SER':
        return {
            'id': data['id'],
            'file': str(data['file']),
            'size': size,
            'can_download': data['can_download']
        }
    elif data_notation == 'OBJ':
        return {
            'id': data.pk,
            'file': base_url + str(data.file),
            'size': float(data.file.size) / 1000000000,
            'can_download': data.can_download
        }


def get_video_study_material_data(data, data_notation, base_url):
    """
    Creates and returns video study material data,
    size is in GB
    """
    response = dict()
    if data_notation == 'OBJ':
        response['id'] = data.id
        response['size'] = float(data.file.size) / 1000000000
        response['can_download'] = data.can_download
        response['bit_rate'] = data.bit_rate
        response['duration'] = data.duration
        response['error_transcoding'] = data.error_transcoding

        if data.stream_file:
            response['stream_file'] = base_url + str(data.stream_file)

        if data.can_download or data.error_transcoding:
            response['file'] = base_url + str(data.file)

    return response


def get_pdf_study_material_data(data, data_notation, base_url, size=None):
    """
    Creates and returns pdf content data dict,
    size is in GB
    """
    if data_notation == 'SER':
        return {
            'id': data['id'],
            'file': str(data['file']),
            'size': size,
            'can_download': data['can_download']
        }
    elif data_notation == 'OBJ':
        return {
            'id': data.pk,
            'file': base_url + str(data.file),
            'size': float(data.file.size) / 1000000000,
            'can_download': data.can_download
        }


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
        if not models.InstitutePermission.objects.filter(
            invitee=self.request.user.pk,
            role=models.InstituteRole.ADMIN
        ).exists():
            return Response({'error': _('Invalid permission')},
                            status=status.HTTP_400_BAD_REQUEST)

        coupon_code = request.data.get('coupon_code')

        if not coupon_code:
            return Response({'error': _('Coupon code is required.')},
                            status=status.HTTP_400_BAD_REQUEST)

        coupon = models.InstituteDiscountCoupon.objects.filter(
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
        licenses = models.InstituteLicense.objects.all()
        monthly_license = licenses.filter(
            billing=models.Billing.MONTHLY).order_by('type')
        yearly_license = licenses.filter(
            billing=models.Billing.ANNUALLY).order_by('type')

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

        if not models.InstitutePermission.objects.filter(
            invitee=self.request.user.pk,
            role=models.InstituteRole.ADMIN
        ).exists():
            return Response({'error': 'Unauthorized request.'},
                            status=status.HTTP_400_BAD_REQUEST)

        license_ = models.InstituteLicense.objects.filter(pk=id_).values()

        if license_:
            return Response(license_[0], status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'License not Found'
            }, status=status.HTTP_400_BAD_REQUEST)


class InstituteSelectLicenseView(APIView):
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

        institute = models.Institute.objects.filter(
            institute_slug=institute_slug
        ).first()
        if not institute:
            return Response({'error': _('Invalid request.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not models.InstitutePermission.objects.filter(
            institute=institute.pk,
            invitee=self.request.user.pk,
            active=True,
            role=models.InstituteRole.ADMIN
        ):
            return Response({'error': _('Insufficient permission.')},
                            status=status.HTTP_400_BAD_REQUEST)
        coupon = None
        if coupon_code:
            coupon = models.InstituteDiscountCoupon.objects.filter(
                coupon_code=coupon_code
            ).first()

            if not coupon.active:
                return Response({'coupon_code': _('Coupon already used.')},
                                status=status.HTTP_400_BAD_REQUEST)
            if timezone.now() > coupon.expiry_date:
                return Response({'coupon_code': _('Coupon expired.')},
                                status=status.HTTP_400_BAD_REQUEST)

        license_ = models.InstituteLicense.objects.filter(
            pk=license_id
        ).first()
        if not license_:
            return Response({'error': _('License not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            sel_lic = models.InstituteSelectedLicense.objects.create(
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
                return Response({'status': _('SUCCESS'),
                                 'net_amount': sel_lic.net_amount,
                                 'selected_license_id': sel_lic.id},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': _('Internal server error.')},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': _('Internal server error.')},
                            status=status.HTTP_400_BAD_REQUEST)


class InstituteCreateOrderView(APIView):
    """View for creating order"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        institute_slug = request.data.get('institute_slug')
        license_id = request.data.get('license_id')
        payment_gateway = request.data.get('payment_gateway')

        errors = {}
        if not institute_slug:
            errors['institute_slug'] = _('This field is required.')
        if not license_id:
            errors['license_id'] = _('This field is required.')
        if not payment_gateway:
            errors['payment_gateway'] = _('This field is required.')

        if errors:
            return Response(
                errors, status=status.HTTP_400_BAD_REQUEST)

        institute = models.Institute.objects.filter(
            institute_slug=institute_slug
        ).first()
        if not institute:
            return Response({'error': _('Invalid request.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not models.InstitutePermission.objects.filter(
                institute=institute.pk,
                invitee=self.request.user.pk,
                active=True,
                role=models.InstituteRole.ADMIN
        ):
            return Response({'error': _('Insufficient permission.')},
                            status=status.HTTP_400_BAD_REQUEST)

        license_ = models.InstituteSelectedLicense.objects.filter(
            pk=license_id
        ).first()
        if not license_:
            return Response({'error': _('Selected license not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if payment_gateway != models.PaymentGateway.RAZORPAY:
            return Response({'error': _('Payment gateway not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        prev_order = models.InstituteLicenseOrderDetails.objects.filter(
            institute=institute,
            selected_license=license_
        ).first()
        if prev_order:
            if prev_order.payment_gateway != payment_gateway:
                prev_order.payment_gateway = payment_gateway
                # Generate order with new payment gateway
                prev_order.save()
            return Response(
                {'status': 'SUCCESS',
                 'amount': prev_order.amount,
                 'key_id': os.environ.get('RAZORPAY_TEST_KEY_ID'),
                 'currency': prev_order.currency,
                 'order_id': prev_order.order_id,
                 'order_details_id': prev_order.pk,
                 'email': str(self.request.user),
                 'contact': str(self.request.user.user_profile.phone),
                 'type': prev_order.selected_license.type},
                status=status.HTTP_201_CREATED)

        try:
            order = models.InstituteLicenseOrderDetails.objects.create(
                institute=institute,
                payment_gateway=payment_gateway,
                selected_license=license_
            )
            if order:
                return Response(
                    {'status': 'SUCCESS',
                     'amount': order.amount,
                     'key_id': os.environ.get('RAZORPAY_TEST_KEY_ID'),
                     'currency': order.currency,
                     'order_id': order.order_id,
                     'order_details_id': order.pk,
                     'email': str(self.request.user),
                     'contact': str(self.request.user.user_profile.phone),
                     'type': order.selected_license.type},
                    status=status.HTTP_201_CREATED)
            else:
                return Response({'error': _('Internal server error.')},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            return Response({'error': _('Internal server error.')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RazorpayPaymentCallbackView(APIView):
    """
    View for storing payment callback data
    and checking whether payment was successful
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        params_dict = {
            'razorpay_order_id': request.data.get('razorpay_order_id'),
            'razorpay_payment_id': request.data.get('razorpay_payment_id'),
            'razorpay_signature': request.data.get('razorpay_signature')
        }
        order_details_id = request.data.get('order_details_id')

        if not params_dict['razorpay_order_id'] and\
                not params_dict['razorpay_payment_id'] and\
                not params_dict['razorpay_signature'] and\
                not order_details_id:
            return Response({'error': _('Invalid fields. Contact support.')},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            order = models.InstituteLicenseOrderDetails.objects.filter(pk=order_details_id).first()
            if not order:
                return Response({
                    'error': _('Order not found. If payment is successful it will be verified automatically.')},
                                status=status.HTTP_400_BAD_REQUEST)
            if order.paid:
                return Response({'status': 'SUCCESS'}, status=status.HTTP_200_OK)

            models.RazorpayCallback.objects.create(
                razorpay_order_id=params_dict['razorpay_order_id'],
                razorpay_payment_id=params_dict['razorpay_payment_id'],
                razorpay_signature=params_dict['razorpay_signature'],
                institute_license_order_details=order)

            try:
                client.utility.verify_payment_signature(params_dict)
                order.paid = True
                order.payment_date = timezone.now()
                order.save()
                return Response({'status': _('SUCCESS')},
                                status=status.HTTP_200_OK)
            except SignatureVerificationError:
                return Response({'status': _('FAILURE')},
                                status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': _('Internal server error. Dont worry, if payment was successful it will be verified automatically. If problem persists let us know.')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RazorpayWebhookCallbackView(APIView):

    def post(self, request, *args, **kwargs):
        request_body = request.body.decode('utf-8')
        try:
            razorpay_order_id = request.data['payload']['payment']['entity']['order_id']
            razorpay_payment_id = request.data['payload']['payment']['entity']['id']
            order = models.InstituteLicenseOrderDetails.objects.filter(order_id=razorpay_order_id).first()
            if not order:
                return Response({'status': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            if order.paid:
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client.utility.verify_webhook_signature(
                request_body,
                request.META.get('HTTP_X_RAZORPAY_SIGNATURE'),
                os.environ.get('RAZORPAY_WEBHOOK_SECRET'))
            order.paid = True
            order.payment_date = timezone.now()
            order.save()
            models.RazorpayWebHookCallback.objects.create(
                order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id
            )
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except SignatureVerificationError:
            return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)


class InstituteLicenseOrderDetailsView(APIView):
    """View for getting list of license orders"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def _get_license_details(self, selected_license):
        """Used to add license details"""
        return {
            'id': selected_license.pk,
            'type': selected_license.type,
            'billing': selected_license.billing,
            'net_amount': float(selected_license.net_amount),
            'storage': selected_license.storage,
            'no_of_admin': selected_license.no_of_admin,
            'no_of_staff': selected_license.no_of_staff,
            'no_of_faculty': selected_license.no_of_faculty,
            'no_of_student': selected_license.no_of_student,
            'video_call_max_attendees': selected_license.video_call_max_attendees,
            'classroom_limit': selected_license.classroom_limit,
            'department_limit': selected_license.department_limit,
            'discussion_forum': selected_license.discussion_forum,
            'scheduled_test': selected_license.scheduled_test,
            'LMS_exists': selected_license.LMS_exists,
        }

    def get(self, *args, **kwargs):
        """
        View for getting active_license, expired_license
        and purchased_inactive_license details by admin.
        """
        institute = models.Institute.objects.filter(
            institute_slug=kwargs.get('institute_slug')
        ).first()

        if not institute:
            return Response({'error': _('Invalid institute.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not models.InstitutePermission.objects.filter(
            institute=institute,
            invitee=self.request.user,
            active=True,
            role=models.InstituteRole.ADMIN
        ).exists():
            return Response({'error': _('Insufficient permission.')},
                            status=status.HTTP_400_BAD_REQUEST)

        orders = models.InstituteLicenseOrderDetails.objects.filter(
            institute=institute,
            paid=True
        )
        active_license = orders.filter(
            active=True,
            end_date__gte=timezone.now()).first()
        purchased_inactive_license = orders.filter(
            active=False,
            end_date=None).first()
        expired_license = orders.filter(
            active=False,
            end_date__lte=timezone.now()).first()
        response = {}
        if not active_license:
            response['active_license'] = {}
        else:
            response['active_license'] = {
                'payment_date': str(active_license.payment_date),
                'start_date': str(active_license.start_date),
                'end_date': str(active_license.end_date),
                'license_details': self._get_license_details(
                    active_license.selected_license)
            }

        if not purchased_inactive_license:
            response['purchased_inactive_license'] = {}
        else:
            response['purchased_inactive_license'] = {
                'payment_date': str(purchased_inactive_license.payment_date),
                'license_details': self._get_license_details(
                    purchased_inactive_license.selected_license)
            }

        if not expired_license:
            response['expired_license'] = {}
        else:
            response['expired_license'] = {
                'payment_date': str(expired_license.payment_date),
                'start_date': str(expired_license.start_date),
                'end_date': str(expired_license.end_date),
                'license_details': self._get_license_details(
                    expired_license.selected_license)
            }

        return Response(response, status=status.HTTP_200_OK)


class InstituteUnexpiredPaidLicenseExistsView(APIView):
    """View for checking whether unexpired license exists"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def get(self, *args, **kwargs):
        """
        Returns true if unexpired license exists else false.
        Only institute permitted user can make call to this api.
        """
        institute = models.Institute.objects.filter(
            institute_slug=kwargs.get('institute_slug')
        ).first()
        if not institute:
            return Response({'error': 'Institute not found.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not models.InstitutePermission.objects.filter(
            institute=institute,
            invitee=self.request.user
        ).exists():
            return Response({'error': 'Permission denied.'},
                            status=status.HTTP_400_BAD_REQUEST)

        order = models.InstituteLicenseOrderDetails.objects.filter(
            institute=institute,
            paid=True
        ).order_by('-payment_date').first()
        if not order or (order.active and order.end_date < timezone.now()):
            return Response({'status': False}, status=status.HTTP_200_OK)
        else:
            return Response({'status': True}, status=status.HTTP_200_OK)


class InstituteMinDetailsTeacherView(ListAPIView):
    """
    View for getting the min details of institute
    by admin teacher
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = serializer.InstituteMinDetailsSerializer
    queryset = models.Institute.objects.all()

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
    queryset = models.Institute.objects.all()

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
    queryset = models.Institute.objects.all()

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
    queryset = models.Institute.objects.all()
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
        institute = models.Institute.objects.filter(
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
        elif role not in [models.InstituteRole.STAFF, models.InstituteRole.FACULTY, models.InstituteRole.ADMIN]:
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
        inviter_perm = models.InstitutePermission.objects.filter(
            institute=institute,
            invitee=inviter,
            active=True
        ).first()
        license_ = get_unexpired_license(institute)

        if not license_:
            return Response({'error': _('License expired or not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        stat = models.InstituteStatistics.objects.filter(institute=institute).first()

        if role == models.InstituteRole.STAFF:
            if stat.no_of_staffs >= license_.selected_license.no_of_staff:
                return Response({'error': _('Max no of staffs already invited.')},
                                status=status.HTTP_400_BAD_REQUEST)
        elif role == models.InstituteRole.FACULTY:
            if stat.no_of_faculties >= license_.selected_license.no_of_faculty:
                return Response({'error': _('Max no of faculties already invited.')},
                                status=status.HTTP_400_BAD_REQUEST)
        elif role == models.InstituteRole.ADMIN:
            if stat.no_of_admins >= license_.selected_license.no_of_admin:
                return Response({'error': _('Max no of admins already invited.')},
                                status=status.HTTP_400_BAD_REQUEST)

        # For assigning admin or staff role
        if role == models.InstituteRole.ADMIN or role == models.InstituteRole.STAFF:
            if not inviter_perm or \
                    inviter_perm.role != models.InstituteRole.ADMIN:
                return Response({'error': _('Insufficient permission.')},
                                status=status.HTTP_400_BAD_REQUEST)

            existing_invite = models.InstitutePermission.objects.filter(
                institute=institute,
                invitee=invitee
            ).first()

            if existing_invite and role == models.InstituteRole.ADMIN:
                if existing_invite.role == models.InstituteRole.ADMIN and not existing_invite.active:
                    return Response({'invitee': _('User already invited.')},
                                    status=status.HTTP_400_BAD_REQUEST)
                if existing_invite.role == models.InstituteRole.ADMIN and existing_invite.active:
                    msg = _('User already has admin permission.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == models.InstituteRole.STAFF:
                    msg = _('Remove staff permission and try again.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == models.InstituteRole.FACULTY:
                    msg = _('Remove faculty permission and try again.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
            elif existing_invite and role == models.InstituteRole.STAFF:
                if existing_invite.role == models.InstituteRole.STAFF and not existing_invite.active:
                    msg = _('User already invited.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == models.InstituteRole.STAFF and existing_invite.active:
                    msg = _('User already has staff permission.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == models.InstituteRole.ADMIN and existing_invite.active:
                    msg = _('Unauthorised. User is admin.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == models.InstituteRole.ADMIN and not existing_invite.active:
                    msg = _('Unauthorised. User was requested to be admin.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == models.InstituteRole.FACULTY:
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
                    if role == models.InstituteRole.ADMIN:
                        stat.no_of_admins += 1
                    else:
                        stat.no_of_staffs += 1
                    stat.save()
                    return Response(response, status=status.HTTP_200_OK)
                except Exception:
                    msg = _('Internal server error. Please contact Eduweb')
                    return Response({'error': msg},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        # For assigning faculty role
        elif role == models.InstituteRole.FACULTY:
            if not inviter_perm or \
                    inviter_perm.role == models.InstituteRole.FACULTY:
                return Response({'error': _('Insufficient permission.')},
                                status=status.HTTP_400_BAD_REQUEST)

            existing_invite = models.InstitutePermission.objects.filter(
                institute=institute,
                invitee=invitee
            ).first()

            if existing_invite:
                if existing_invite.role == models.InstituteRole.FACULTY and not existing_invite.active:
                    return Response({'invitee': _('User already invited.')},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == models.InstituteRole.FACULTY and existing_invite.active:
                    return Response({'invitee': _('User is already a faculty.')},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == models.InstituteRole.ADMIN and not existing_invite.active:
                    msg = _('Unauthorized. User was already requested for admin role.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == models.InstituteRole.ADMIN and existing_invite.active:
                    msg = _('Unauthorized. User has admin permissions.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == models.InstituteRole.STAFF and not existing_invite.active:
                    msg = _('Unauthorized. User was already requested for staff role.')
                    return Response({'invitee': msg},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif existing_invite.role == models.InstituteRole.STAFF and existing_invite.active:
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
                    stat.no_of_faculties += 1
                    stat.save()
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
        institute = models.Institute.objects.filter(
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
            invitation = models.InstitutePermission.objects.filter(
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

                invitation = models.InstitutePermission.objects.filter(
                    institute=institute,
                    invitee=invitee
                ).first()

                if not invitation:
                    msg = _('Invitation not found or already deleted.')
                    return Response({'error': msg},
                                    status=status.HTTP_400_BAD_REQUEST)

                inviter = models.InstitutePermission.objects.filter(
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
                if inviter.role != models.InstituteRole.ADMIN or\
                        invitation.active and inviter.role == invitation.role:
                    return Response({'error': _('Permission denied.')},
                                    status=status.HTTP_400_BAD_REQUEST)

                try:
                    role = invitation.role
                    invitation.delete()
                    stat = models.InstituteStatistics.objects.filter(
                        institute=institute
                    ).first()
                    if role == models.InstituteRole.FACULTY:
                        stat.no_of_faculties -= 1
                    elif role == models.InstituteRole.STAFF:
                        stat.no_of_staffs -= 1
                    elif role == models.InstituteRole.ADMIN:
                        stat.no_of_admins -= 1
                    stat.save()
                    return Response({'status': 'DELETED'},
                                    status=status.HTTP_200_OK)
                except Exception:
                    msg = _('Internal Server Error. Please contact EduWeb.')
                    return Response({'error': msg},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Invitee is trying to delete join request
            else:
                invitation = models.InstitutePermission.objects.filter(
                    institute=institute,
                    invitee=self.request.user
                ).first()

                if not invitation:
                    msg = _('Invitation not found or already deleted.')
                    return Response({'error': msg},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Deleting invitation
                try:
                    role = invitation.role
                    invitation.delete()
                    stat = models.InstituteStatistics.objects.filter(
                        institute=institute
                    ).first()
                    if role == models.InstituteRole.FACULTY:
                        stat.no_of_faculties -= 1
                    elif role == models.InstituteRole.STAFF:
                        stat.no_of_staffs -= 1
                    elif role == models.InstituteRole.ADMIN:
                        stat.no_of_admins -= 1
                    stat.save()
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
        institute = models.Institute.objects.filter(
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

        has_perm = models.InstitutePermission.objects.filter(
            institute=institute,
            invitee=self.request.user,
            active=True
        ).exists()

        if not has_perm:
            return Response({'error': _('Permission denied.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if role == 'ADMIN':
            permitted_user_invitations = models.InstitutePermission.objects.filter(
                institute=institute,
                role=models.InstituteRole.ADMIN
            )
            response_data = {
                'active_admin_list': self._format_data(
                    permitted_user_invitations.filter(active=True)),
                'pending_admin_invites': self._format_data(
                    permitted_user_invitations.filter(active=False), False)
            }
            return Response(response_data, status=status.HTTP_200_OK)
        elif role == 'STAFF':
            permitted_user_invitations = models.InstitutePermission.objects.filter(
                institute=institute,
                role=models.InstituteRole.STAFF
            )
            response_data = {
                'active_staff_list': self._format_data(
                    permitted_user_invitations.filter(active=True)),
                'pending_staff_invites': self._format_data(
                    permitted_user_invitations.filter(active=False), False)
            }
            return Response(response_data, status=status.HTTP_200_OK)
        elif role == 'FACULTY':
            permitted_user_invitations = models.InstitutePermission.objects.filter(
                institute=institute,
                role=models.InstituteRole.FACULTY
            )
            response_data = {
                'active_faculty_list': self._format_data(
                    permitted_user_invitations.filter(active=True)),
                'pending_faculty_invites': self._format_data(
                    permitted_user_invitations.filter(active=False), False)
            }
            return Response(response_data, status=status.HTTP_200_OK)


class CreateClassView(CreateAPIView):
    """View to creating institute class"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher,)
    serializer_class = serializer.InstituteClassSerializer

    def create(self, request, *args, **kwargs):
        institute = models.Institute.objects.filter(
            institute_slug=kwargs.get('institute_slug')
        ).first()

        if not institute:
            return Response({'error': _('Institute not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not models.InstitutePermission.objects.filter(
            institute=institute,
            invitee=self.request.user,
            active=True,
            role=models.InstituteRole.ADMIN
        ).exists():
            return Response({'error': _('Permission denied.')},
                            status=status.HTTP_400_BAD_REQUEST)

        license_ = models.InstituteLicenseOrderDetails.objects.filter(
            institute=institute,
            paid=True
        ).order_by('-payment_date').first()

        if not license_ or (license_.active and license_.end_date < timezone.now()):
            return Response({'error': _('License expired or not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        ins_stat = models.InstituteStatistics.objects.filter(institute=institute).first()
        if ins_stat.class_count >= license_.selected_license.classroom_limit:
            return Response({'error': _('Maximum class creation limit attained.')},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer_ = self.get_serializer(data={
            'class_institute': institute.pk,
            'name': request.data.get('name')
        })
        if serializer_.is_valid():
            serializer_.save()
            ins_stat.class_count += 1
            ins_stat.save()
            response = serializer_.data
            response['class_incharges'] = list()
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteClassView(DestroyAPIView):
    """View for deleting class"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher,)

    def destroy(self, request, *args, **kwargs):
        """Only active admin or permitted staff can delete"""
        class_ = models.InstituteClass.objects.filter(
            class_slug=kwargs.get('class_slug')
        ).first()

        if not class_:
            return Response(status=status.HTTP_204_NO_CONTENT)

        institute = models.Institute.objects.filter(
            pk=class_.class_institute.pk).first()

        if institute:
            permission = models.InstitutePermission.objects.filter(
                institute=institute,
                invitee=self.request.user,
                active=True
            ).first()

            if not permission or\
                    permission.role == models.InstituteRole.FACULTY or\
                    permission.role == models.InstituteRole.STAFF and\
                    not models.InstituteClassPermission.objects.filter(
                        invitee=self.request.user, to=class_
                    ).exists():
                return Response({'error': 'Permission denied.'},
                                status=status.HTTP_400_BAD_REQUEST)
            class_.delete()
            stat = models.InstituteStatistics.objects.filter(
                institute=institute
            ).first()
            stat.class_count -= 1
            stat.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Institute not found.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListAllClassView(APIView):
    """View for listing all classes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher,)

    def get(self, request, *args, **kwargs):
        institute = models.Institute.objects.filter(
            institute_slug=kwargs.get('institute_slug')
        ).first()

        if not institute:
            return Response({'error': _('Invalid Institute.')},
                            status=status.HTTP_400_BAD_REQUEST)

        perm = models.InstitutePermission.objects.filter(
            institute=institute,
            invitee=self.request.user,
            active=True
        ).first()

        if not perm:
            return Response({'error': _('Permission denied.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not get_unexpired_license(institute):
            return Response({'error': _('License expired or not purchased.')},
                            status=status.HTTP_400_BAD_REQUEST)

        queryset = models.InstituteClass.objects.filter(
            class_institute=institute
        ).order_by('created_on')
        response = []

        for data in queryset:
            class_details = dict()
            class_details['id'] = data.id
            class_details['name'] = data.name
            class_details['class_slug'] = data.class_slug
            class_details['created_on'] = data.created_on
            class_ = models.InstituteClass.objects.filter(
                class_slug=data.class_slug).first()
            if perm and perm.role == models.InstituteRole.ADMIN or\
                    models.InstituteClassPermission.objects.filter(
                        invitee=self.request.user, to=class_).exists():
                class_details['has_class_perm'] = True
            else:
                class_details['has_class_perm'] = False

            class_incharges = list()
            incharges = models.InstituteClassPermission.objects.filter(
                to=class_
            ).order_by('created_on')

            for incharge in incharges:
                incharge_details = dict()
                incharge_details['id'] = incharge.invitee.pk
                incharge_details['email'] = str(incharge.invitee)
                invitee = get_user_model().objects.filter(pk=incharge.invitee.pk).first()
                invitee = models.UserProfile.objects.filter(
                    user=invitee
                ).first()
                incharge_details['name'] = invitee.first_name + ' ' + invitee.last_name
                class_incharges.append(incharge_details)

            class_details['class_incharges'] = class_incharges
            response.append(class_details)

        return Response(response, status=status.HTTP_200_OK)


class ProvideClassPermissionView(CreateAPIView):
    """View for providing class permission by admin to staff/admin"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher,)

    def create(self, request, *args, **kwargs):
        class_ = models.InstituteClass.objects.filter(
            class_slug=request.data.get('class_slug')
        ).first()

        if not class_:
            return Response({'error': _('Class not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        institute = models.Institute.objects.filter(
            pk=class_.class_institute.pk).first()

        if not models.InstitutePermission.objects.filter(
            institute=institute,
            active=True,
            invitee=self.request.user,
            role=models.InstituteRole.ADMIN
        ).exists():
            return Response({'error': _('Permission denied.')},
                            status=status.HTTP_400_BAD_REQUEST)

        invitee = get_user_model().objects.filter(
            email=request.data.get('invitee')
        ).first()

        if not invitee:
            return Response({'error': _('This user does not exist.')},
                            status=status.HTTP_400_BAD_REQUEST)

        invitee_perm = models.InstitutePermission.objects.filter(
            institute=institute,
            active=True,
            invitee=invitee
        ).first()

        if not invitee_perm:
            return Response({'error': _('User is not a member of this institute.')},
                            status=status.HTTP_400_BAD_REQUEST)
        elif invitee_perm.role == models.InstituteRole.FACULTY:
            return Response({'error': _('Faculty can not be provided class permission.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if models.InstituteClassPermission.objects.filter(
                to=class_,
                invitee=invitee).exists():
            return Response({'error': _('User already has class permission.')},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            perm = models.InstituteClassPermission.objects.create(
                invitee=invitee,
                inviter=self.request.user,
                to=class_
            )
            invitee = get_object_or_404(models.UserProfile,
                                        user=invitee)
            inviter = get_object_or_404(models.UserProfile,
                                        user=self.request.user)
            return Response({
                'id': perm.id,
                'invitee_id': perm.invitee.pk,
                'name': invitee.first_name + ' ' + invitee.last_name,
                'email': str(invitee),
                'inviter_name': inviter.first_name + ' ' + inviter.last_name,
                'inviter_email': str(inviter),
                'created_on': str(perm.created_on),
                'image': None
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': _('User is already class incharge.')},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': _('Internal server error.')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListPermittedClassInchargeView(APIView):
    """View for listing all permitted class incharges"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher,)

    def get(self, *args, **kwargs):
        class_ = models.InstituteClass.objects.filter(
            class_slug=kwargs.get('class_slug')
        ).first()

        if not class_:
            return Response({'error': _('Class not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not models.InstitutePermission.objects.filter(
            institute=models.Institute.objects.filter(
                pk=class_.class_institute.pk).first(),
            active=True,
            invitee=self.request.user
        ).exists():
            return Response({'error': _('Permission denied.')},
                            status=status.HTTP_400_BAD_REQUEST)

        response = []
        perm = models.InstituteClassPermission.objects.filter(
            to=class_
        ).order_by('created_on')
        for p in perm:
            res = dict()
            invitee = models.UserProfile.objects.filter(
                user=get_user_model().objects.filter(
                    pk=p.invitee.pk).first()).first()
            inviter = None
            if p.inviter:
                inviter = models.UserProfile.objects.filter(
                    user=get_user_model().objects.filter(
                        pk=p.inviter.pk).first()).first()
            res['id'] = p.id
            res['invitee_id'] = p.invitee.pk
            res['name'] = invitee.first_name + ' ' + invitee.last_name
            res['email'] = str(p.invitee)
            if inviter:
                res['inviter_name'] = inviter.first_name + ' ' + inviter.last_name
                res['inviter_email'] = str(p.inviter)
            else:
                res['inviter_name'] = 'Anonymous'
                res['inviter_email'] = ' '
            res['created_on'] = str(p.created_on)
            res['image'] = None
            response.append(res)
        return Response(response, status=status.HTTP_200_OK)


class CheckClassPermView(APIView):
    """View returns true if user has class perm"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def get(self, *args, **kwargs):
        class_ = models.InstituteClass.objects.filter(
            class_slug=kwargs.get('class_slug')
        ).first()

        if not class_:
            return Response({'error': _('Class not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        perm = models.InstitutePermission.objects.filter(
            institute=models.Institute.objects.filter(
                pk=class_.class_institute.pk).first(),
            invitee=self.request.user,
            active=True
        ).first()

        if not perm:
            return Response({'error': _('Permission denied.')},
                            status=status.HTTP_400_BAD_REQUEST)
        elif perm.role == models.InstituteRole.FACULTY:
            return Response({'status': False},
                            status=status.HTTP_200_OK)
        elif perm.role == models.InstituteRole.ADMIN:
            return Response({'status': True},
                            status=status.HTTP_200_OK)
        else:
            if models.InstituteClassPermission.objects.filter(
                to=class_,
                invitee=self.request.user
            ).exists():
                return Response({'status': True},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': False},
                                status=status.HTTP_200_OK)


class CreateSubjectView(APIView):
    """View for creating subject"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        class_ = models.InstituteClass.objects.filter(
            class_slug=kwargs.get('class_slug')
        ).first()

        if not class_:
            return Response({'error': _('Class not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('name'):
            return Response({'error': _('Subject name is required.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('type'):
            return Response({'error': _('Subject type is required.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('name').strip():
            return Response({'error': _('Subject name can not be blank.')},
                            status=status.HTTP_400_BAD_REQUEST)

        has_perm = models.InstituteClassPermission.objects.filter(
            to=class_,
            invitee=self.request.user
        ).exists()

        if not has_perm:
            if not models.InstitutePermission.objects.filter(
                institute=models.Institute.objects.filter(
                    pk=class_.class_institute.pk).first(),
                invitee=self.request.user,
                active=True,
                role=models.InstituteRole.ADMIN
            ).exists():
                return Response({'error': _('Permission denied.')},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            subject = models.InstituteSubject.objects.create(
                subject_class=class_,
                name=self.request.data.get('name'),
                type=self.request.data.get('type')
            )
            return Response({
                'id': subject.id,
                'name': subject.name,
                'type': subject.type,
                'created_on': subject.created_on,
                'subject_incharges': []
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': _('Subject with same name exists.')},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': _('Internal server error.')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListAllSubjectView(APIView):
    """View for listing all subjects"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def get(self, *args, **kwargs):
        class_ = models.InstituteClass.objects.filter(
            class_slug=kwargs.get('class_slug')
        ).first()

        if not class_:
            return Response({'error': _('Class not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        institute = models.Institute.objects.filter(
                pk=class_.class_institute.pk).first()
        perm = models.InstitutePermission.objects.filter(
            institute=institute,
            invitee=self.request.user,
            active=True
        ).first()

        if not perm:
            return Response({'error': _('Permission denied.')},
                            status=status.HTTP_400_BAD_REQUEST)

        subject_list = models.InstituteSubject.objects.filter(
            subject_class=class_
        ).filter().order_by('created_on')
        response = []
        for sub in subject_list:
            subject_details = dict()
            subject_details['id'] = sub.id
            subject_details['name'] = sub.name
            subject_details['subject_slug'] = sub.subject_slug
            subject_details['type'] = sub.type
            subject_details['created_on'] = sub.created_on
            if perm and perm.role == models.InstituteRole.ADMIN:
                subject_details['has_subject_perm'] = True
            else:
                institute_subject = models.InstituteSubject.objects.filter(
                    subject_slug=sub.subject_slug).first()
                if models.InstituteSubjectPermission.objects.filter(
                    to=institute_subject,
                    invitee=self.request.user
                ).exists():
                    subject_details['has_subject_perm'] = True
                else:
                    subject_details['has_subject_perm'] = False
            subject_incharges = list()
            incharges = models.InstituteSubjectPermission.objects.filter(
                to=sub
            ).order_by('created_on')

            for perm_ in incharges:
                incharge_details = dict()
                incharge_details['id'] = perm_.invitee.pk
                incharge_details['email'] = str(perm_.invitee)
                invitee = get_user_model().objects.filter(
                    pk=perm_.invitee.pk).first()
                invitee = models.UserProfile.objects.filter(
                    user=invitee).first()
                incharge_details['name'] = invitee.first_name + ' ' + invitee.last_name
                subject_incharges.append(incharge_details)

            subject_details['subject_incharges'] = subject_incharges
            response.append(subject_details)
        return Response(response, status=status.HTTP_200_OK)


class ListSubjectInstructorsView(APIView):
    """View for listing all class instructors"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def get(self, *args, **kwargs):
        subject = models.InstituteSubject.objects.filter(
            subject_slug=kwargs.get('subject_slug')
        ).first()

        if not subject:
            return Response({'error': _('Subject not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        class_ = models.InstituteClass.objects.get(
            pk=subject.subject_class.pk)
        institute = models.Institute.objects.get(
            pk=class_.class_institute.pk)

        if not models.InstitutePermission.objects.filter(
            institute=institute,
            invitee=self.request.user,
            active=True
        ).exists():
            return Response({'error': _('Permission denied.')},
                            status=status.HTTP_400_BAD_REQUEST)

        perm_list = models.InstituteSubjectPermission.objects.filter(
            to=subject
        ).order_by('created_on')
        response = []

        for perm in perm_list:
            invite_details = dict()
            invite_details['id'] = perm.id
            invite_details['invitee_id'] = perm.invitee.pk
            invite_details['email'] = str(perm.invitee)
            invitee = get_user_model().objects.filter(
                pk=perm.invitee.pk).first()
            invitee = models.UserProfile.objects.filter(
                user=invitee).first()

            if perm.inviter:
                inviter = get_user_model().objects.filter(
                    pk=perm.inviter.pk).first()
                inviter = models.UserProfile.objects.filter(
                    user=inviter).first()
                invite_details['inviter_name'] = inviter.first_name + ' ' + inviter.last_name
                invite_details['inviter_email'] = str(perm.inviter)
            else:
                invite_details['inviter_name'] = ' '
                invite_details['inviter_email'] = ' '

            invite_details['name'] = invitee.first_name + ' ' + invitee.last_name
            invite_details['created_on'] = str(perm.created_on)
            invite_details['image'] = None
            response.append(invite_details)

        return Response(response, status=status.HTTP_200_OK)


class AddSubjectPermissionView(APIView):
    """View for adding subject permission"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        subject = models.InstituteSubject.objects.filter(
            subject_slug=request.data.get('subject_slug')
        ).first()

        if not subject:
            return Response({'error': _('Subject not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        class_ = models.InstituteClass.objects.filter(
            pk=subject.subject_class.pk).first()
        institute = models.Institute.objects.filter(
            pk=class_.class_institute.pk).first()
        has_perm = models.InstituteClassPermission.objects.filter(
            to=class_,
            invitee=self.request.user
        ).exists()

        if not has_perm:
            if not models.InstitutePermission.objects.filter(
                institute=institute,
                invitee=self.request.user,
                active=True,
                role=models.InstituteRole.ADMIN
            ).exists():
                return Response({'error': _('Permission denied.')},
                                status=status.HTTP_400_BAD_REQUEST)

        invitee = get_user_model().objects.filter(
            email=request.data.get('invitee')
        ).first()

        if not invitee:
            return Response({'error': _('This user does not exist.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not models.InstitutePermission.objects.filter(
            institute=institute,
            invitee=invitee,
            active=True
        ).exists():
            return Response({'error': _('User is not a member of this institute.')},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            perm = models.InstituteSubjectPermission.objects.create(
                to=subject,
                inviter=self.request.user,
                invitee=invitee
            )
            invitee = models.UserProfile.objects.filter(user=invitee).first()
            inviter = models.UserProfile.objects.filter(user=self.request.user).first()
            return Response({
                'email': str(perm.invitee),
                'name': invitee.first_name + ' ' + invitee.last_name,
                'invitee_id': perm.invitee.pk,
                'inviter_email': str(perm.inviter),
                'inviter_name': inviter.first_name + ' ' + inviter.last_name,
                'created_on': str(perm.created_on),
                'image': None
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': _('User is already an instructor.')},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': _('Internal Server Error.')},
                            status=status.HTTP_400_BAD_REQUEST)


class CreateSectionView(APIView):
    """View for creating section"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        class_ = models.InstituteClass.objects.filter(
            class_slug=kwargs.get('class_slug')
        ).first()

        if not class_:
            return Response({'error': _('Class not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('name'):
            return Response({'error': _('Section name is required.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('name').strip():
            return Response({'error': _('Section name can not be blank.')},
                            status=status.HTTP_400_BAD_REQUEST)

        has_perm = models.InstituteClassPermission.objects.filter(
            to=class_,
            invitee=self.request.user
        ).exists()

        if not has_perm:
            institute = models.Institute.objects.filter(
                pk=class_.class_institute.pk).first()
            if not models.InstitutePermission.objects.filter(
                institute=institute,
                invitee=self.request.user,
                active=True,
                role=models.InstituteRole.ADMIN
            ).exists():
                return Response({'error': _('Permission denied.')},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            section = models.InstituteSection.objects.create(
                section_class=class_,
                name=self.request.data.get('name')
            )
            return Response({
                'name': section.name,
                'section_slug': section.section_slug,
                'created_on': section.created_on,
                'section_incharges': []
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': _('Section with same name exists.')},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': _('Internal server error.')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddSectionPermissionView(APIView):
    """View for adding section permission"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        section = models.InstituteSection.objects.filter(
            section_slug=request.data.get('section_slug')
        ).first()

        if not section:
            return Response({'error': _('Section not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        class_ = models.InstituteClass.objects.filter(
            pk=section.section_class.pk).first()
        institute = models.Institute.objects.filter(
            pk=class_.class_institute.pk).first()
        has_perm = models.InstituteClassPermission.objects.filter(
            to=class_,
            invitee=self.request.user
        ).exists()

        if not has_perm:
            if not models.InstitutePermission.objects.filter(
                institute=institute,
                invitee=self.request.user,
                active=True,
                role=models.InstituteRole.ADMIN
            ).exists():
                return Response({'error': _('Permission denied.')},
                                status=status.HTTP_400_BAD_REQUEST)

        invitee = get_user_model().objects.filter(
            email=request.data.get('invitee')
        ).first()

        if not invitee:
            return Response({'error': _('This user does not exist.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not models.InstitutePermission.objects.filter(
            institute=institute,
            invitee=invitee,
            active=True
        ).exists():
            return Response({'error': _('User is not a member of this institute.')},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            perm = models.InstituteSectionPermission.objects.create(
                to=section,
                inviter=self.request.user,
                invitee=invitee
            )
            invitee = models.UserProfile.objects.filter(user=invitee).first()
            inviter = models.UserProfile.objects.filter(user=self.request.user).first()
            return Response({
                'email': str(perm.invitee),
                'name': invitee.first_name + ' ' + invitee.last_name,
                'invitee_id': perm.invitee.pk,
                'inviter_email': str(perm.inviter),
                'inviter_name': inviter.first_name + ' ' + inviter.last_name,
                'created_on': str(perm.created_on),
                'image': None
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': _('User already has section permission.')},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': _('Internal Server Error.')},
                            status=status.HTTP_400_BAD_REQUEST)


class ListAllSectionView(APIView):
    """View for listing all section"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def get(self, *args, **kwargs):
        class_ = models.InstituteClass.objects.filter(
            class_slug=kwargs.get('class_slug')
        ).first()

        if not class_:
            return Response({'error': _('Class not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        perm = models.InstitutePermission.objects.filter(
            institute=models.Institute.objects.filter(
                pk=class_.class_institute.pk).first(),
            invitee=self.request.user,
            active=True
        ).first()

        if not perm:
            return Response({'error': _('Permission denied.')},
                            status=status.HTTP_400_BAD_REQUEST)

        section_list = models.InstituteSection.objects.filter(
            section_class=class_
        ).filter().order_by('created_on')
        response = []
        for section in section_list:
            section_details = dict()
            section_details['id'] = section.id
            section_details['name'] = section.name
            section_details['section_slug'] = section.section_slug
            section_details['created_on'] = section.created_on
            sec = models.InstituteSection.objects.filter(
                section_slug=section.section_slug).first()

            if perm and perm.role == models.InstituteRole.ADMIN:
                section_details['has_section_perm'] = True
            else:
                if models.InstituteSectionPermission.objects.filter(
                    to=sec,
                    invitee=self.request.user
                ).exists():
                    section_details['has_section_perm'] = True
                else:
                    section_details['has_section_perm'] = False

            section_incharges = list()
            invites = models.InstituteSectionPermission.objects.filter(
                to=sec
            )

            for invite in invites:
                incharge_details = dict()
                invitee = get_user_model().objects.filter(pk=invite.invitee.pk).first()
                invitee = models.UserProfile.objects.filter(user=invitee).first()
                incharge_details['id'] = invite.invitee.pk
                incharge_details['email'] = str(invite.invitee)
                incharge_details['name'] = invitee.first_name + ' ' + invitee.last_name
                section_incharges.append(incharge_details)

            section_details['section_incharges'] = section_incharges
            response.append(section_details)
        return Response(response, status=status.HTTP_200_OK)


class ListSectionInchargesView(APIView):
    """View for listing all section incharges"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def get(self, *args, **kwargs):
        section = models.InstituteSection.objects.filter(
            section_slug=kwargs.get('section_slug')
        ).first()

        if not section:
            return Response({'error': _('Section not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        class_ = models.InstituteClass.objects.get(pk=section.section_class.pk)
        institute = models.Institute.objects.get(pk=class_.class_institute.pk)

        if not models.InstitutePermission.objects.filter(
            institute=institute,
            invitee=self.request.user,
            active=True
        ).exists():
            return Response({'error': _('Permission denied.')},
                            status=status.HTTP_400_BAD_REQUEST)

        perm_list = models.InstituteSectionPermission.objects.filter(
            to=section
        ).order_by('created_on')
        response = []

        for perm in perm_list:
            invite_details = dict()
            invite_details['id'] = perm.id
            invite_details['email'] = str(perm.invitee)
            invite_details['invitee_id'] = perm.invitee.pk
            invitee = get_user_model().objects.filter(pk=perm.invitee.pk).first()
            invitee = models.UserProfile.objects.filter(user=invitee).first()

            if perm.inviter:
                inviter = get_user_model().objects.filter(pk=perm.inviter.pk).first()
                inviter = models.UserProfile.objects.filter(user=inviter).first()
                invite_details['inviter_name'] = inviter.first_name + ' ' + inviter.last_name
                invite_details['inviter_email'] = str(perm.inviter)
            else:
                invite_details['inviter_name'] = ' '
                invite_details['inviter_email'] = ' '

            invite_details['name'] = invitee.first_name + ' ' + invitee.last_name
            invite_details['created_on'] = str(perm.created_on)
            invite_details['image'] = None
            response.append(invite_details)

        return Response(response, status=status.HTTP_200_OK)


class InstituteSubjectAddCourseContentView(APIView):
    """Creates institute subject add course content view"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)
    parser_classes = (JSONParser, MultiPartParser)

    def _validate_image_file(self, file):
        """Checking whether the file is an image file"""
        try:
            if not file:
                return Response({'error': _('File is required.')},
                                status=status.HTTP_400_BAD_REQUEST)
            Image.open(file).verify()
        except Exception:
            return Response({'error': _(
                'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')},
                            status=status.HTTP_400_BAD_REQUEST)

    def _validate_video_file(self, file):
        """Checking whether the file is video file"""
        try:
            if not file:
                return Response({'error': _('File is required.')},
                                status=status.HTTP_400_BAD_REQUEST)
            elif not filetype.is_video(file):
                return Response({'error': _('Not a valid video file.')},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': _('Error occurred.')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_pdf_file(self, file, raw_file):
        """Checking whether the file is pdf file"""
        try:
            if not file:
                return Response({'error': _('File is required.')},
                                status=status.HTTP_400_BAD_REQUEST)
            elif not filetype.is_archive(file):
                return Response({'error': _('Not a valid pdf file.')},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                kind = os.path.splitext(raw_file)[1]
                if not kind.endswith('.pdf'):
                    return Response({'error': _('Not a valid pdf file.')},
                                    status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': _('An internal error occurred')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        subject = models.InstituteSubject.objects.filter(
            subject_slug=kwargs.get('subject_slug')).first()

        if not subject:
            return Response({'error': _('Subject not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not models.InstituteSubjectPermission.objects.filter(
            to=subject,
            invitee=self.request.user
        ).exists():
            return Response({'error': _('Permission denied.')},
                            status=status.HTTP_400_BAD_REQUEST)

        subject_stats = models.InstituteSubjectStatistics.objects.filter(
            statistics_subject=subject
        ).first()

        if request.data.get('description'):
            description = request.data.get('description')
        else:
            description = ' '

        course_content_serializer = serializer.SubjectCourseContentCreateSerializer(
            data={
                'title': request.data.get('title'),
                'content_type': request.data.get('content_type'),
                'view': request.data.get('view'),
                'order': subject_stats.max_order + 1,
                'target_date': request.data.get('target_date'),
                'course_content_subject': subject.pk,
                'description': description
            })

        if course_content_serializer.is_valid():
            course_content_serializer.save()
        else:
            return Response(course_content_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        response = get_study_material_content_details(course_content_serializer.data, 'SER')

        if request.data.get('content_type') == models.StudyMaterialContentType.EXTERNAL_LINK:
            url = request.data.get('url')

            if not url:
                return Response({'error': _('Url is required')},
                                status=status.HTTP_400_BAD_REQUEST)

            external_link_serializer = serializer.SubjectExternalLinkStudyMaterialSerializer(
                data={
                    'external_link_study_material': course_content_serializer.data['id'],
                    'url': url
                })
            if external_link_serializer.is_valid():
                external_link_serializer.save()
                subject_stats.max_order += 1
                subject_stats.save()

                response_data = get_external_link_study_material_data(external_link_serializer.data, 'SER')
                response['data'] = response_data
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                models.InstituteSubjectCourseContent.objects.filter(
                    pk=course_content_serializer.data['id']).first().delete()
                return Response(external_link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            # try:
            size = request.data.get('size')

            if not size:
                models.InstituteSubjectCourseContent.objects.filter(
                    pk=course_content_serializer.data['id']).first().delete()
                return Response({'error': _('Error occurred. ERROR_CODE: SIZE. Please contact us.')},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                size = Decimal(size)

            class_ = models.InstituteClass.objects.filter(pk=subject.subject_class.pk).first()
            institute = models.Institute.objects.filter(pk=class_.class_institute.pk).first()
            institute_stats = get_institute_stats_and_validate(institute, size)

            if not isinstance(institute_stats, models.InstituteStatistics):
                models.InstituteSubjectCourseContent.objects.filter(
                    pk=course_content_serializer.data['id']).first().delete()
                return institute_stats

            # Image file
            if request.data.get('content_type') == models.StudyMaterialContentType.IMAGE:
                validate = self._validate_image_file(request.data.get('file'))

                if validate:
                    models.InstituteSubjectCourseContent.objects.filter(
                        pk=course_content_serializer.data['id']).first().delete()
                    return validate

                image_serializer = serializer.ImageStudyMaterialSerializer(
                    data={
                        'image_study_material': course_content_serializer.data['id'],
                        'file': request.data.get('file'),
                        'can_download': request.data.get('can_download')
                    }, context={"request": request})

                if image_serializer.is_valid():
                    image_serializer.save()
                    subject_stats.max_order += 1
                    subject_stats.storage += size
                    subject_stats.save()
                    institute_stats.storage += size
                    institute_stats.save()

                    response['data'] = get_image_study_material_data(
                        image_serializer.data,
                        'SER',
                        self.request.build_absolute_uri('/').strip("/") + MEDIA_URL,
                        float(size)
                    )
                    return Response(response, status=status.HTTP_201_CREATED)
                else:
                    models.InstituteSubjectCourseContent.objects.filter(
                        pk=course_content_serializer.data['id']).first().delete()
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Video file
            elif request.data.get('content_type') == models.StudyMaterialContentType.VIDEO:
                validate = self._validate_video_file(request.data.get('file'))

                if validate:
                    models.InstituteSubjectCourseContent.objects.filter(
                        pk=course_content_serializer.data['id']).first().delete()
                    return validate

                video_serializer = serializer.VideoStudyMaterialSerializer(
                    data={
                        'video_study_material': course_content_serializer.data['id'],
                        'file': request.data.get('file'),
                        'can_download': request.data.get('can_download')
                    }, context={"request": request})

                if video_serializer.is_valid():
                    video_serializer.save()
                    subject_stats.max_order += 1
                    subject_stats.storage += size
                    subject_stats.save()
                    institute_stats.storage += size
                    institute_stats.save()

                    # Creating steamable files
                    file_obj = models.SubjectVideoStudyMaterial.objects.filter(
                        pk=video_serializer.data['id']).first()

                    try:
                        video_file_path = MEDIA_ROOT + '/' + str(file_obj.file)
                        video = ffmpeg_streaming.input(video_file_path)

                        ffprobe = FFProbe(video_file_path)
                        video_format = ffprobe.format()
                        duration = video_format['duration']
                        bit_rate = video_format['bit_rate']

                        _144p = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
                        _240p = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
                        _360p = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
                        _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
                        _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
                        abs_file_path = models.hls_encoded_video_saving_file_name_path(str(file_obj.file))
                        rel_file_path = abs_file_path.replace(MEDIA_ROOT, '').strip('//')
                        hls_key_saving_abs_path = (models.hls_key_saving_path(str(file_obj.file)))
                        hls_key_saving_rel_path = hls_key_saving_abs_path.replace(MEDIA_ROOT, '').strip('//')
                        url = self.request.build_absolute_uri('/').strip("/") + MEDIA_URL + hls_key_saving_rel_path

                        hls = video.hls(Formats.h264())
                        hls.representations(_144p, _240p, _360p, _480p, _720p)
                        hls.encryption(hls_key_saving_abs_path, url, 5)
                        hls.output(abs_file_path, monitor=monitor)

                        file_obj.duration = Decimal(duration)
                        file_obj.bit_rate = bit_rate
                        file_obj.stream_file = rel_file_path
                        file_obj.save()

                        response['data'] = get_video_study_material_data(
                            file_obj,
                            'OBJ',
                            self.request.build_absolute_uri('/').strip("/") + MEDIA_URL
                        )
                    except Exception:
                        file_obj.error_transcoding = True
                        file_obj.save()
                        raise Exception()

                    return Response(response, status=status.HTTP_201_CREATED)
                else:
                    models.InstituteSubjectCourseContent.objects.filter(
                        pk=course_content_serializer.data['id']).first().delete()
                    return Response(video_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Pdf file
            elif request.data.get('content_type') == models.StudyMaterialContentType.PDF:
                validate = self._validate_pdf_file(request.data.get('file'), str(request.FILES['file']))

                if validate:
                    models.InstituteSubjectCourseContent.objects.filter(
                        pk=course_content_serializer.data['id']).first().delete()
                    return validate

                pdf_serializer = serializer.PdfStudyMaterialSerializer(
                    data={
                        'pdf_study_material': course_content_serializer.data['id'],
                        'file': request.data.get('file'),
                        'can_download': request.data.get('can_download')
                    }, context={"request": request})

                if pdf_serializer.is_valid():
                    pdf_serializer.save()
                    subject_stats.max_order += 1
                    subject_stats.storage += size
                    subject_stats.save()
                    institute_stats.storage += size
                    institute_stats.save()
                    response['data'] = get_pdf_study_material_data(
                        pdf_serializer.data,
                        'SER',
                        self.request.build_absolute_uri('/').strip("/") + MEDIA_URL,
                        float(size)
                    )

                    return Response(response, status=status.HTTP_201_CREATED)
                else:
                    models.InstituteSubjectCourseContent.objects.filter(
                        pk=course_content_serializer.data['id']).first().delete()
                    return Response(pdf_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # except Exception:
            #     models.InstituteSubjectCourseContent.objects.filter(
            #         pk=course_content_serializer.data['id']).first().delete()
            #     return Response({'error': _('Error occurred.')},
            #                     status=status.HTTP_400_BAD_REQUEST)


class InstituteSubjectMinStatisticsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def get(self, *args, **kwargs):
        """Get institute statistics"""
        subject = models.InstituteSubject.objects.filter(
            subject_slug=kwargs.get('subject_slug')
        ).first()

        if not subject:
            return Response({'error': 'Subject not found.'},
                            status=status.HTTP_400_BAD_REQUEST)

        class_ = models.InstituteClass.objects.filter(pk=subject.subject_class.pk).first()
        institute = models.Institute.objects.filter(pk=class_.class_institute.pk).first()

        if not models.InstituteSubjectPermission.objects.filter(
            to=subject,
            invitee=self.request.user
        ).exists():
            if not models.InstitutePermission.objects.filter(
                institute=institute,
                role=models.InstituteRole.ADMIN,
                invitee=self.request.user,
                active=True,
            ).exists():
                return Response({'error': 'Permission denied.'},
                                status=status.HTTP_400_BAD_REQUEST)
        order = get_unexpired_license(institute)

        if not order:
            return Response({'error': _('License expired or not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        response = dict()
        response['storage'] = dict()
        response['storage']['total_storage'] = float(order.selected_license.storage)
        response['storage']['storage_used'] = float(models.InstituteStatistics.objects.filter(
            institute=institute
        ).first().storage)

        views = models.SubjectViewNames.objects.filter(
            view_subject=subject
        ).order_by('order')

        view_order = list()
        view_details = dict()

        for view in views:
            view_order.append(view.key)
            subject_view_model = models.SubjectViewNames.objects.filter(
                view_subject=subject,
                key=view.key
            ).first()
            view_details[view.key] = {
                'name': view.name,
                'count': models.InstituteSubjectCourseContent.objects.filter(
                    course_content_subject=subject,
                    view=subject_view_model
                ).count()
            }
            if view.key != 'MI' and view.key != 'CO':
                weeks = models.SubjectViewWeek.objects.filter(
                    week_view=view
                ).order_by('value')
                for week in weeks:
                    view_details[view.key][week.value] = models.InstituteSubjectCourseContent.objects.filter(
                        course_content_subject=subject,
                        view=subject_view_model,
                        week=week
                    ).count()

        response['view_order'] = view_order
        response['view_details'] = view_details

        return Response(response, status=status.HTTP_200_OK)


class InstituteSubjectSpecificViewCourseContentView(APIView):
    """View for getting course content of a specific subject view"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def get(self, *args, **kwargs):
        subject = models.InstituteSubject.objects.filter(
            subject_slug=kwargs.get('subject_slug').lower()
        ).first()

        if not subject:
            return Response({'error': 'Subject not found.'},
                            status=status.HTTP_400_BAD_REQUEST)

        class_ = models.InstituteClass.objects.filter(pk=subject.subject_class.pk).first()
        institute = models.Institute.objects.filter(pk=class_.class_institute.pk).first()

        if not models.InstituteSubjectPermission.objects.filter(
                to=subject,
                invitee=self.request.user
        ).exists():
            if not models.InstitutePermission.objects.filter(
                    institute=institute,
                    role=models.InstituteRole.ADMIN,
                    invitee=self.request.user,
                    active=True,
            ).exists():
                return Response({'error': _('Permission denied.')},
                                status=status.HTTP_400_BAD_REQUEST)

        data = models.InstituteSubjectCourseContent.objects.filter(
            course_content_subject=subject,
            view=kwargs.get('view').upper()
        ).order_by('order')
        response = list()

        for d in data:
            res = get_study_material_content_details(d, 'OBJ')

            if d.content_type == models.StudyMaterialContentType.EXTERNAL_LINK:
                query_data = models.SubjectExternalLinkStudyMaterial.objects.filter(
                    external_link_study_material__pk=d.id
                ).first()
                res['data'] = get_external_link_study_material_data(
                    query_data,
                    'OBJ'
                )
            elif d.content_type == models.StudyMaterialContentType.IMAGE:
                query_data = models.SubjectImageStudyMaterial.objects.filter(
                        image_study_material__pk=d.id
                    ).first()
                res['data'] = get_image_study_material_data(
                    query_data,
                    'OBJ',
                    self.request.build_absolute_uri('/').strip("/") + MEDIA_URL
                )
            elif d.content_type == models.StudyMaterialContentType.VIDEO:
                query_data = models.SubjectVideoStudyMaterial.objects.filter(
                        video_study_material__pk=d.id
                    ).first()
                res['data'] = get_video_study_material_data(
                    query_data,
                    'OBJ',
                    self.request.build_absolute_uri('/').strip("/") + MEDIA_URL
                )
            elif d.content_type == models.StudyMaterialContentType.PDF:
                query_data = models.SubjectPdfStudyMaterial.objects.filter(
                        pdf_study_material__pk=d.id
                    ).first()
                res['data'] = get_pdf_study_material_data(
                    query_data,
                    'OBJ',
                    self.request.build_absolute_uri('/').strip("/") + MEDIA_URL
                )
            response.append(res)

        return Response(response, status=status.HTTP_200_OK)


class InstituteDeleteSubjectCourseContentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def delete(self, request, *args, **kwargs):
        course_content = models.InstituteSubjectCourseContent.objects.filter(
            pk=kwargs.get('pk')
        ).first()

        if not course_content:
            return Response(status=status.HTTP_204_NO_CONTENT)

        subject = models.InstituteSubject.objects.filter(
            pk=course_content.course_content_subject.pk
        ).first()
        class_ = models.InstituteClass.objects.filter(pk=subject.subject_class.pk).first()
        institute = models.Institute.objects.filter(pk=class_.class_institute.pk).first()

        if not models.InstituteSubjectPermission.objects.filter(
                to=subject,
                invitee=self.request.user
        ).exists():
            if not models.InstitutePermission.objects.filter(
                    institute=institute,
                    role=models.InstituteRole.ADMIN,
                    invitee=self.request.user,
                    active=True,
            ).exists():
                return Response({'error': _('Permission denied.')},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            if course_content.content_type == models.StudyMaterialContentType.EXTERNAL_LINK:
                models.SubjectExternalLinkStudyMaterial.objects.filter(
                    external_link_study_material__pk=course_content.pk).first().delete()
                course_content.delete()
            else:
                subject_stat = models.InstituteSubjectStatistics.objects.filter(
                    statistics_subject=subject
                ).first()
                institute_stat = models.InstituteStatistics.objects.filter(
                    institute=institute
                ).first()
                size = 0
                if course_content.content_type == models.StudyMaterialContentType.IMAGE:
                    file_data = models.SubjectImageStudyMaterial.objects.filter(
                        image_study_material__pk=course_content.pk).first()
                    size = file_data.file.size/1000000000 # In Gb
                    file_data.delete()
                elif course_content.content_type == models.StudyMaterialContentType.VIDEO:
                    file_data = models.SubjectVideoStudyMaterial.objects.filter(
                        video_study_material__pk=course_content.pk).first()
                    size = file_data.file.size / 1000000000 # In Gb
                    file_data.delete()
                elif course_content.content_type == models.StudyMaterialContentType.PDF:
                    file_data = models.SubjectPdfStudyMaterial.objects.filter(
                        pdf_study_material__pk=course_content.pk).first()
                    size = file_data.file.size / 1000000000 # In Gb
                    file_data.delete()
                course_content.delete()
                subject_stat.storage = max(0, subject_stat.storage - Decimal(size))
                subject_stat.save()
                institute_stat.storage = max(0, institute_stat.storage - Decimal(size))
                institute_stat.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response({'error': _('Internal server error. Kindly refresh and try again.')},
                            status=status.HTTP_400_BAD_REQUEST)


class InstituteSubjectEditCourseContentView(APIView):
    """View for modifying course content details"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)

    def patch(self, request, *args, **kwargs):
        subject = models.InstituteSubject.objects.filter(
            subject_slug=kwargs.get('subject_slug').lower()
        ).first()

        if not subject:
            return Response({'error': _('Subject not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        study_material = models.InstituteSubjectCourseContent.objects.filter(
            pk=kwargs.get('pk')
        ).first()

        if not study_material:
            return Response({'error': _('Study material not found.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if not models.InstituteSubjectPermission.objects.filter(
            to=subject,
            invitee=self.request.user
        ).exists():
            return Response({'error': _('Permission denied.')},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('title'):
            study_material.title = request.data.get('title')
        if request.data.get('description'):
            study_material.description = request.data.get('description')
        if 'target_date' in request.data.keys():
            if request.data.get('target_date'):
                study_material.target_date = request.data.get('target_date')
            else:
                study_material.target_date = None

        try:
            study_material.save()
            response = get_study_material_content_details(study_material, 'OBJ')
            if request.data.get('content_type') == models.StudyMaterialContentType.EXTERNAL_LINK:
                content = models.SubjectExternalLinkStudyMaterial.objects.filter(
                    external_link_study_material=study_material
                ).first()
                content.url = request.data.get('data')['url']
                content.save()
                response['data'] = get_external_link_study_material_data(content, 'OBJ')
            elif request.data.get('content_type') == models.StudyMaterialContentType.VIDEO:
                content = models.SubjectVideoStudyMaterial.objects.filter(
                    video_study_material=study_material
                ).first()
                content.can_download = request.data.get('data')['can_download']
                content.save()
                response['data'] = get_video_study_material_data(
                    content,
                    'OBJ',
                    self.request.build_absolute_uri('/').strip("/") + MEDIA_URL
                )
            elif request.data.get('content_type') == models.StudyMaterialContentType.PDF:
                content = models.SubjectPdfStudyMaterial.objects.filter(
                    pdf_study_material=study_material
                ).first()
                content.can_download = request.data.get('data')['can_download']
                content.save()
                response['data'] = get_pdf_study_material_data(
                    content,
                    'OBJ',
                    self.request.build_absolute_uri('/').strip("/") + MEDIA_URL
                )
            elif request.data.get('content_type') == models.StudyMaterialContentType.IMAGE:
                content = models.SubjectImageStudyMaterial.objects.filter(
                    image_study_material=study_material
                ).first()
                content.can_download = request.data.get('data')['can_download']

                print(content.can_download)
                content.save()
                response['data'] = get_image_study_material_data(
                    content,
                    'OBJ',
                    self.request.build_absolute_uri('/').strip("/") + MEDIA_URL
                )

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'Bad Request'},
                            status=status.HTTP_400_BAD_REQUEST)
