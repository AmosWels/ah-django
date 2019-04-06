from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.articles.models import Article
from authors.apps.articles.tests.test_data import valid_article
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import valid_user


class CreateArticleAPIViewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(**valid_user)

        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.data = valid_article

    def test_api_can_create_an_article_with_authenticated_user(self):
        article = self.data

        response = self.client.post(
            '/api/articles/',
            {"article": article},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_cannot_create_an_article_with_an_unauthenticated_user(self):
        self.client.logout()

        article = self.data

        response = self.client.post(
            '/api/articles/',
            {"article": article},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
