from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .app_urls import register_url, login_url, activate_url, user_action_url
from .test_data import valid_user, invalid_token


class UserRetrieveUpdateAPIViewTestCase(TestCase):
    """
    This class defines the test suite for the view
    that retrieves and updates a user
    """

    def setUp(self):
        self.client = APIClient()

        response = self.client.post(
            register_url, {"user": valid_user}, format="json")

        self.token = response.data["data"]["token"]

        self.client.get(f"{activate_url}?token={self.token}", format='json')

        response = self.client.post(
            login_url, {"user": valid_user}, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_verify_account_with_invalid_token(self):
        self.client.get(f"{activate_url}?token={invalid_token}", format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + invalid_token)
        response = self.client.get(user_action_url, format="json")
        self.assertIn(
            "Invalid authentication. Could not decode token.",
            response.data["errors"]["detail"])

    def test_invalid_verification_link(self):
        response = self.client.get(f"{activate_url}?token={invalid_token}", format='json')
        self.assertIn(
            "Verifcation link is invalid. Check email for correct link.",
            response.data["errors"]["detail"])

    def test_api_can_retrieve_a_registered_user(self):

        response = self.client.get(user_action_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_needs_authentication_to_retrieve_a_user(self):

        self.client.logout()

        response = self.client.get(user_action_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_update_user_data(self):

        new_user_data = {
            "email": "jjones@email.com",
            "bio": "I like eggs for breakfast",
            "image": "https://myimages.com/erwt.png"}

        response = self.client.put(
            user_action_url, {"user": new_user_data}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_needs_authentication_to_update_user_data(self):
        new_user_data = {
            "email": "jjones@email.com",
            "bio": "I like eggs for breakfast",
            "image": "https://myimages.com/erwt.png"}

        self.client.logout()

        response = self.client.put(
            user_action_url, {"user": new_user_data}, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_get_user_data_with_bad_authorization_header(self):
        response = self.client.post(
            login_url, {"user": valid_user}, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Fred ' + self.token)
        response = self.client.get(login_url, format="json")
        self.assertIn("Bad Authorization header.", response.data["errors"]["detail"])

    def test_api_get_user_data_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + invalid_token)
        response = self.client.get(user_action_url, format="json")
        self.assertIn(
            "Invalid authentication. Could not decode token.",
            response.data["errors"]["detail"])
