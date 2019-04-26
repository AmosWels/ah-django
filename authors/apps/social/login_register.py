from rest_framework.response import Response
from rest_framework import status, exceptions
from django.core.exceptions import ValidationError

from authors.apps.authentication.models import User

def login_or_register_social_user(social_user):

    try:
        user = User.objects.get(email=social_user.get('email'))

        return {
                'email': user.email, 
                'username': user.username, 
                'token': user.token
            }

    except User.DoesNotExist:
        if social_user.get("email") is None:
            raise ValidationError("Users must have an email address.")
        
        new_social_user = {
            'email': social_user.get('email'),
            'username': social_user.get('name', "unknown"),
            'password': User.objects.make_random_password()
        }

        new_user = User.objects.create_user(**new_social_user)
        new_user.is_active = True
        new_user.save()

        return {
                'email': social_user.get('email'), 
                'username': social_user.get('name'),
                'token': new_user.token
            }
