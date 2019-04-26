import os
import facebook
import twitter
from google.oauth2 import id_token
from google.auth.transport import requests

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .exceptions import SocialAuthenticationFailed
from .login_register import login_or_register_social_user
from authors.apps.authentication.renderers import UserJSONRenderer

class FacebookAuthAPIView(CreateAPIView):
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        facebook_token = request.data.get('user', {})
        access_token = facebook_token.get("access_token", {})
        try:
            graph = facebook.GraphAPI(access_token=access_token)
            facebook_user = graph.get_object(id='me', fields='email, name')
        except:
            raise SocialAuthenticationFailed
        response =  login_or_register_social_user(facebook_user)
        return Response(response, status=status.HTTP_200_OK)


class GoogleAuthAPIView(CreateAPIView):
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        google_token = request.data.get('user', {})
        access_token = google_token.get("access_token", {})
        try:
            google_user = id_token.verify_oauth2_token(
                access_token, requests.Request())
        except:
            raise SocialAuthenticationFailed
        response = login_or_register_social_user(google_user)
        return Response(response, status=status.HTTP_200_OK)


class TwitterAuthAPIView(CreateAPIView):
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        twitter_tokens = request.data.get('user', {})
        try:
            api = twitter.Api(
                consumer_key= os.getenv("TWITTER_CONSUMER_KEY", ""),
                consumer_secret= os.getenv("TWITTER_CONSUMER_SECRET", ""),
                access_token_key=twitter_tokens.get("access_token", ''),
                access_token_secret=twitter_tokens.get("access_token_secret", '')
            )
            twitter_user = api.VerifyCredentials(include_email=True)
            twitter_user = twitter_user.__dict__
        except:
            raise SocialAuthenticationFailed

        respose = login_or_register_social_user(twitter_user)
        return Response(respose, status=status.HTTP_200_OK)
