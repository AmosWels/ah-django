from rest_framework import status, exceptions
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from datetime import datetime, timedelta

from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer
)

from django.core.mail import send_mail

import os
import jwt


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")

        url = f"{BASE_URL}/api/users/verify?token={serializer.data['token']}"

        subject = 'Activate your Authors Haven account'
        body = f"Hi {serializer.data['username']}, \
                     \nThanks for signing up for Authors Haven account!' \
                     '\nPlease confirm your account by clicking the link below. \
                         \n{url} \
                         \n\nThe Aqua Team."
        send_mail(
            subject, body,
            'noreply@aqua.com',
            [serializer.data["email"]],
            fail_silently=True
        )
        data = {
            "message": "Account created! Check your email to activate this account.",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        user_data = request.data.get('user', {})

        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),
    
            'profile': {
                'bio': user_data.get('bio', request.user.profile.bio),
                'image': user_data.get('image', request.user.profile.image)
            }
        }
        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivateAccount(APIView):
    def get(self, request):
        token = request.query_params.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            msg = 'Verficaton link expired. Sign up again.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = 'Verifcation link is invalid. Check email for correct link.'
            raise exceptions.AuthenticationFailed(msg)

        user = User.objects.filter(username=payload['usn'])
        user.update(is_active=True)
        return Response(
            {"message": "Your Email has been verified,you can now login"}, 
            status.HTTP_200_OK
        )


class ResetPasswordView(APIView):
    def post(self, request):
        try:
            if not request.data["email"]:
                raise exceptions.ValidationError("Email address should not be empty")
            token = jwt.encode({
                'email': request.data["email"],
                'exp': datetime.utcnow() + timedelta(hours=1)
            }, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

            BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")

            url = f"{BASE_URL}/api/users/new-password/?token={token}"

            subject = 'Authors Haven account. Password recovery'
            body = f"We have recieved a request to reset your password. \
                        \nUse the link below to set up a new password for your account. \
                        \nIf you did not request to reset your password, ignore this email. \
                            \n{url} \
                            \n\nThe Aqua Team."
            send_mail(
                subject, body,
                'noreply@aqua.com',
                [request.data["email"]],
                fail_silently=True
            )
            data = {
                "message": "Please check your email for recovery password link.",
                "status": status.HTTP_201_CREATED
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except KeyError:
            raise exceptions.ValidationError("Email field required to reset password")

class NewPasswordView(APIView):
    def patch(self, request):
        try:
            password = request.data["password"]
            if len(password) < 8:
                raise exceptions.ValidationError(
                    "Password length must be greater than 7 characters")
            token = request.query_params.get('token')
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.filter(email=payload["email"]).first()
            user.set_password(password)
            user.save()
            return Response({
                "message": "Your password has been changed successfully",
                "status": status.HTTP_200_OK
            })
        except jwt.ExpiredSignatureError:
            raise exceptions.ParseError(
                "Verficaton link expired. Reset password again.", 
                )
        except jwt.InvalidTokenError:
            raise exceptions.ParseError(
                "Verifcation link is invalid. Check email for correct link.", 
                )
        except KeyError:
            raise exceptions.ValidationError("Password field required to change password")
