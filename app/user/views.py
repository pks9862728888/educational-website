from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser

from .serializer import CreateUserSerializer, LoginUserSerializer,\
    UploadUserProfilePictureSerializer, SetUserProfilePictureSerializer,\
    ListProfilePictureSerializer

from core.models import ProfilePictures


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


class ListProfilePictureView(ListAPIView):
    """View for listing all profile pictures"""
    serializer_class = ListProfilePictureSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = ProfilePictures.objects.all()

    def get_object(self):
        """Returns only images of the logged in user"""
        return self.request.user

    def get_queryset(self):
        """Applies filter to show images of only logged in user"""
        queryset = self.queryset.filter(user=self.request.user)
        return queryset


class UploadProfilePictureView(APIView):
    """View for uploading profile picture"""
    serializer_class = UploadUserProfilePictureSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    parser_classes = [JSONParser, MultiPartParser]

    def post(self, request, format=None):
        """To save the profile picture"""
        user = get_user_model().objects.get(email=request.user)
        serialize = self.serializer_class(data=request.data,
                                          context={"request": request})

        class_profile_picture = request.data.get('class_profile_picture')
        public_profile_picture = request.data.get('public_profile_picture')

        if serialize.is_valid():
            # Setting previous image to inactive
            previous_images = ProfilePictures.objects.filter(user=user)

            if class_profile_picture:
                previous_images = previous_images.filter(
                    class_profile_picture=True)

            if public_profile_picture:
                previous_images = previous_images.filter(
                    public_profile_picture=True)

            if not (public_profile_picture or class_profile_picture):
                return Response({
                    "non-field-errors": [
                        "Select where you want to set profile picture."
                    ]
                }, status=status.HTTP_400_BAD_REQUEST)

            # Setting pervious image to inactive if present
            for image in previous_images:
                img = ProfilePictures.objects.get(id=image.id)
                if class_profile_picture:
                    img.class_profile_picture = False

                if public_profile_picture:
                    img.public_profile_picture = False

                img.save()

            serialize.save(user=user)
            return Response(serialize.data, status=status.HTTP_200_OK)
        else:
            return Response(serialize.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class SetDeleteProfilePictureView(APIView):
    """View for setting or deleting profile picture"""
    serializer_class = SetUserProfilePictureSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    parser_classes = [JSONParser, MultiPartParser]

    def post(self, request, format=None):
        """To save the profile picture"""
        user = get_user_model().objects.get(email=request.user)
        id = request.data.get('id', None)
        class_profile_picture = request.data.get(
            'class_profile_picture', None)
        public_profile_picture = request.data.get(
            'public_profile_picture', None)

        errors = {}  # Stores custom validation errors
        if not (public_profile_picture or class_profile_picture):
            errors["non-field-errors"] = [
                    "Select where you want to the set profile picture."
                ]

        # Validating id
        try:
            picture = ProfilePictures.objects.get(id=id)
        except Exception:
            errors['id'] = ['Please send a valid id.']
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if not picture.user == user:
            errors['id'] = ['Please send a valid id.']
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if len(errors):
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # Creating data dict to serialize
        data = {}
        data['id'] = id
        data['image'] = picture.image
        data['uploaded_on'] = picture.uploaded_on
        if public_profile_picture:
            data['public_profile_picture'] = public_profile_picture
        else:
            data['public_profile_picture'] = False

        if class_profile_picture:
            data['class_profile_picture'] = class_profile_picture
        else:
            data['class_profile_picture'] = False

        serialize = self.serializer_class(
            data=data, context={"request": request})

        if serialize.is_valid():
            # Setting previous image to inactive
            previous_images = ProfilePictures.objects.filter(
                user=user)

            if public_profile_picture:
                previous_images = previous_images.filter(
                    public_profile_picture=True)

            if class_profile_picture:
                previous_images = previous_images.filter(
                    class_profile_picture=True)

            for image in previous_images:
                img = ProfilePictures.objects.get(id=image.id)

                if class_profile_picture:
                    img.class_profile_picture = False

                if public_profile_picture:
                    img.public_profile_picture = False

                img.save()

            # Setting current image to active
            if class_profile_picture:
                picture.class_profile_picture = True

            if public_profile_picture:
                picture.public_profile_picture = True

            picture.save()
            return Response(serialize.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serialize.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """To delete profile picture"""
        user = get_user_model().objects.get(email=request.user)

        # Validating id
        try:
            picture = ProfilePictures.objects.get(id=pk)
        except Exception:
            return Response({'id': ['Please send a valid id']},
                            status=status.HTTP_400_BAD_REQUEST)

        if not picture.user == user:
            return Response({'id': ['Please send a valid id']},
                            status=status.HTTP_400_BAD_REQUEST)

        class_profile_picture_ = picture.class_profile_picture
        public_profile_picture_ = picture.public_profile_picture
        try:
            picture.delete()
            return Response(
                {
                    'class_profile_picture_deleted': class_profile_picture_,
                    'public_profile_picture_deleted': public_profile_picture_,
                    'deleted': True
                },
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception:
            return Response(
                {
                    'class_profile_picture_deleted': class_profile_picture_,
                    'public_profile_picture_deleted': public_profile_picture_,
                    'deleted': False
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
