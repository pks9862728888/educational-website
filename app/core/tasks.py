from __future__ import absolute_import, unicode_literals

from celery import shared_task

import os
from django.contrib.auth import get_user_model

from core import models


@shared_task
def create_welcome_message_after_user_creation(receiver_pk):
    """Creates welcome message after user is created"""
    system_user = get_user_model().objects.filter(
        username=os.environ.get('SYSTEM_USER_USERNAME')
    ).first()

    if not system_user:
        system_user = get_user_model().objects.create(
            email=os.environ.get('SYSTEM_USER_EMAIL'),
            username=os.environ.get('SYSTEM_USER_USERNAME'),
            password=os.environ.get('SYSTEM_USER_PASSWORD')
        )

    receiver = get_user_model().objects.get(pk=receiver_pk)

    message = models.SystemMessage.objects.create(
        sender=system_user,
        receiver=receiver,
        title='Welcome message',
        message='Hi ' + receiver.username + ', <br/>' +
                'Welcome to EduWeb and Thank you for signing up.' +
                ' Now you can create' +
                ' institutes, classrooms, or courses' +
                ' as per your requirements.'
    )
    return message.id
