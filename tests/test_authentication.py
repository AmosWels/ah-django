from base64 import b64encode
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework import serializers
from django.core import mail
from django.urls import reverse

from authors.apps.authentication.models import User, UserManager
from authors.apps.authentication.serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer)



class UserTestCase(TestCase):
    """ This class defines the test suite for the user model. """

    def setUp(self):
        self.username = "henryjones"
        self.email = "hjones@email.com"
        self.password = "T35ting-i2E"
        self.user = User(
            username=self.username,
            email=self.email,
            password=self.password)

    def test_model_can_create_a_user(self):

        previous_count = User.objects.count()
        self.user.save()
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertEqual(str(self.user), self.email)

    def test_model_returns_fullname_of_user(self):
        self.user.save()

        self.assertEqual(self.user.get_full_name, self.username)

    def test_model_returns_shortname_of_user(self):
        self.user.save()

        self.assertEqual(self.user.get_short_name(), self.username)


class UserManagerTestCase(TestCase):
    """ This class defines the test suite for the user manager model. """

    def setUp(self):
        self.username = "henryjones"
        self.email = "hjones@email.com"
        self.password = "T35ting-i2E"

    def test_manager_can_create_a_regular_user_with_required_fields(self):
        kwargs = {
            "username": self.username,
            "email": self.email,
            "password": self.password}

        previous_count = User.objects.count()
        user = User.objects.create_user(**kwargs)
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertFalse(user.is_superuser)

    def test_manager_can_create_a_regular_user_without_password_field(self):
        kwargs = {
            "username": self.username,
            "email": self.email}

        user = User.objects.create_user(**kwargs)
        self.assertIsNotNone(user.password)
        self.assertFalse(user.is_superuser)

    def test_manager_cannot_create_a_regular_user_without_username_field(self):
        kwargs = {
            "email": self.email,
            "password": self.password}

        self.assertRaises(TypeError, User.objects.create_user, **kwargs)

    def test_manager_cannot_create_a_regular_user_without_email_field(self):
        kwargs = {
            "username": self.username,
            "password": self.password}

        self.assertRaises(TypeError, User.objects.create_user, **kwargs)

    def test_manager_can_create_a_super_user_with_required_fields(self):
        kwargs = {
            "username": self.username,
            "email": self.email,
            "password": self.password}

        previous_count = User.objects.count()
        user = User.objects.create_superuser(**kwargs)
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertTrue(user.is_superuser)

    def test_manager_cannot_create_a_super_user_without_username_field(self):
        kwargs = {
            "email": self.email,
            "password": self.password}

        self.assertRaises(TypeError, User.objects.create_superuser, **kwargs)

    def test_manager_cannot_create_a_super_user_without_email_field(self):
        kwargs = {
            "username": self.username,
            "password": self.password}

        self.assertRaises(TypeError, User.objects.create_superuser, **kwargs)

    def test_manager_cannot_create_a_super_user_without_password_field(self):
        kwargs = {
            "username": self.username,
            "email": self.email}

        self.assertRaises(TypeError, User.objects.create_superuser, **kwargs)


class RegistrationAPIViewTestCase(TestCase):
    """ This class defines the test suite for the registration view. """

    def setUp(self):

        self.existing_user_data = {
            "username": "janejones",
            "email": "jjones@email.com",
            "password": "Enter-123"}

        self.existing_user = User.objects.create_user(
            **self.existing_user_data)
        self.client = APIClient()

    def test_api_can_create_a_user(self):
        user_data = {
            "username": "henryjones",
            "email":'mwngnchls@gmail.com',
            "password": "Enterwithus12349"}

        response = self.client.post(
            '/api/users/',
            {"user": user_data},
            format="json")
        # print("Response ", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_cannot_create_a_user_with_existing_email(self):

        user_data = {
            "username": "peter",
            "email": self.existing_user_data["email"],
            "password": "Enter123"}

        response = self.client.post(
            '/api/users/',
            {"user": user_data},
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user with this email already exists.",
                      response.data["errors"]["email"], )

    def test_api_cannot_create_a_user_with_existing_username(self):

        user_data = {
            "username": self.existing_user_data["username"],
            "email": "peter@email.com",
            "password": "Enter123"}

        response = self.client.post(
            '/api/users/',
            {"user": user_data},
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user with this username already exists.",
                      response.data["errors"]["username"])

    def test_api_cannot_create_a_user_with_password_lessthan_eight_characters(self):

        user_data = {
            "username": "peter",
            "email": "peter@email.com",
            "password": "Enter"}

        response = self.client.post(
            '/api/users/',
            {"user": user_data},
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Ensure this field has at least 8 characters.",
                      response.data["errors"]["password"])

    def test_api_cannot_create_user_without_alphanumeric_password(self):
        user_data = {
                "username": "peter",
                "email": "peter@email.com",
                "password": "Password"
        }
        response = self.client.post(
            '/api/users/',
            { "user": user_data},
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password must contain a numeric character", response.data["errors"]["password"])

    def test_api_cannot_create_user_with_invalid_email(self):
        user_data = {
                "username": "peter",
                "email": "peter@.com",
                "password": "Password1"
        }
        response = self.client.post(
            '/api/users/',
            { "user": user_data},
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Enter a valid email address.", response.data["errors"]["email"])


class LoginAPIViewTestCase(TestCase):
    """ This class defines the test suite for the login view. """

    def setUp(self):

        self.existing_user_data = {
            "username": "janejones",
            "email": "jjones@email.com",
            "password": "Enter-123"}

        self.existing_user = User.objects.create_user(
            **self.existing_user_data)
        self.client = APIClient()

    def test_api_cannot_login_an_unregistered_user(self):
        user_data = {
            "email": "peter@email.com",
            "password": "Enter-123"}

        response = self.client.post(
            '/api/users/login/',
            {"user": user_data},
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'User not found or account not active.',
            response.data["errors"]['error'])

    def test_api_cannot_login_user_with_valid_email_wrong_password_combination(self):
        user_data = {
            "email": self.existing_user.email,
            "password": "enter-123"}

        response = self.client.post(
            '/api/users/login/',
            {"user": user_data},
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'User not found or account not active.',
            response.data["errors"]["error"]
        )


class UserRetrieveUpdateAPIViewTestCase(TestCase):
    """
    This class defines the test suite for the view
    that retrieves and updates a user
    """

    def setUp(self):
        self.user_data_2 = {
            "username": "nicksbro",
            "email": "nicholus@gmail.com",
            "password": "Enter1234"
            }
        self.user_data = {
            "username": "janejones2",
            "email": "nicholusmuwonge@gmail.com",
            "password": "Enter1234"
            }
        self.activate_url = reverse('authentication:activate-account')
        self.register_url = reverse('authentication:register')
        self.login_url = reverse('authentication:login')
        self.user_action_url = reverse('authentication:user-action')
        self.client = APIClient()
        response = self.client.post(
            self.register_url, {"user": self.user_data_2}, format="json"
            )
        response = self.client.post(
            self.register_url, {"user": self.user_data}, format="json")
        # print("Response ", response.data)
        self.token = response.data["data"]["token"]
        self.client.get(f"{self.activate_url}?token={self.token}", format='json')

        response = self.client.post(
            self.login_url, {"user": self.user_data}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_verify_account_with_invalid_token(self):
        invalid_token = "icVpZnJlZCIsImV4cCI6MTU1ODY3"
        self.client.get(f"{self.activate_url}?token={invalid_token}", format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + invalid_token)
        response = self.client.get(self.user_action_url, format="json")
        self.assertIn(
            "Invalid authentication. Could not decode token.",
            response.data["detail"])

    def test_invalid_verification_link(self):
        invalid_token = "icVpZnJlZCIsImV4cCI6MTU1ODY3"
        response = self.client.get(f"{self.activate_url}?token={invalid_token}", format='json')
        self.assertIn(
            "Verifcation link is invalid. Check email for correct link.",
            response.data["detail"])

    def test_api_can_retrieve_a_registered_user(self):

        response = self.client.get(self.user_action_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_needs_authentication_to_retrieve_a_user(self):

        self.client.logout()

        response = self.client.get(self.user_action_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_update_user_data(self):

        new_user_data = {
            "email": "jjones@email.com",
            "bio": "I like eggs for breakfast",
            "image": "https://myimages.com/erwt.png"}

        response = self.client.put(
            self.user_action_url, {"user": new_user_data}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_needs_authentication_to_update_user_data(self):
        new_user_data = {
            "email": "jjones@email.com",
            "bio": "I like eggs for breakfast",
            "image": "https://myimages.com/erwt.png"}

        self.client.logout()

        response = self.client.put(
            self.user_action_url, {"user": new_user_data}, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_get_user_data_with_bad_authorization_header(self):
        response = self.client.post(
            self.login_url, {
                "user": {"email": "jjones@email.com", "password": "Enter-123"}
                }, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Fred ' + self.token)
        response = self.client.get(self.login_url, format="json")
        self.assertIn("Bad Authorization header.", response.data["detail"])

    def test_api_get_user_data_with_invalid_token(self):
        invalid_token = "icVpZnJlZCIsImV4cCI6MTU1ODY3"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + invalid_token)
        response = self.client.get(self.user_action_url, format="json")
        self.assertIn(
            "Invalid authentication. Could not decode token.",
            response.data["detail"])

    def test_api_can_allow_user_to_view_another_person_status(self):
        new_user_data = {
            "email": "jjones@email.com",
            "bio": "I like eggs for breakfast",
            "image": "https://myimages.com/erwt.png"}
        self.client.put(
            self.user_action_url, {"user": new_user_data}, format="json"
            )

        response = self.client.get(
            '/api/profiles/janejones2',
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("janejones", response.data["username"])
        self.assertIn("https://myimages.com/erwt.png", response.data["image"])

    def test_profile_created_on_user_registration(self):
        
        response = self.client.get(
            '/api/profiles/nicksbro',
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("", response.data["username"])
        self.assertIn("", response.data["image"])

    def test_api_cannot_retrieve_a_non_existing_profile(self):
        response = self.client.get(
            '/api/profiles/jane',
            format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(
            "The requested profile does not exist.",
            response.data["errors"]["detail"])

    def test_api_user_cannot_other_persons_profiles(self):
        new_user_data = {
            "email": "jjones@email.com",
            "bio": "I like eggs for breakfast",
            "image": "https://myimages.com/erwt.png"}
        response = self.client.put(
            '/api/profiles/nicksbro',
            {"user": new_user_data},
            format="json")

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
            )

    def test_user_can_view_their_own_status(self):
        response = self.client.put(
            '/api/user/',
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class LoginSerializerTestCase(TestCase):

    def setUp(self):
        self.user_data = {
            "username": "janejones",
            "email": "jjones@email.com",
            "password": "Enter-123"}
        self.user = User.objects.create_user(**self.user_data)
        self.serializer_class = LoginSerializer
        self.serializer = self.serializer_class(data=self.user_data)

    def test_serializer_can_validate_an_unregisterd_user(self):
        user_data = {
            "username": "hjones",
            "email": "hjones@email.com",
            "password": "Enter-123"}

        serializer = self.serializer_class(data=user_data)
        is_valid_data = serializer.is_valid()

        self.assertFalse(is_valid_data)
        self.assertRaisesMessage(
            serializers.ValidationError,
            'User not found or account not active.',
            serializer.validate,
            user_data)

    def test_serializer_raises_an_exception_on_request_without_an_email(self):
        user_data = {
            "username": "janejones",
            "password": "Enter-123"
        }

        serializer = self.serializer_class(data=user_data)

        self.assertRaises(
            serializers.ValidationError,
            serializer.is_valid,
            raise_exception=True)
        self.assertRaisesMessage(
            serializers.ValidationError,
            'An email address is required to log in.',
            serializer.validate,
            user_data)

    def test_serializer_raises_an_exception_on_request_without_password(self):
        user_data = {
            "username": "jjones",
            "email": "jjones@email.com"}

        serializer = self.serializer_class(data=user_data)

        self.assertRaises(
            serializers.ValidationError,
            serializer.is_valid,
            raise_exception=True)
        self.assertRaisesMessage(
            serializers.ValidationError,
            'A password is required to log in.',
            serializer.validate,
            user_data)
