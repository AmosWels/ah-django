from django.test import TestCase
from rest_framework import serializers

from authors.apps.articles.models import Article
from authors.apps.articles.serializers import CreateArticleSerializer
from authors.apps.articles.tests.test_data import (article_without_body,
                                                   article_without_description,
                                                   article_without_title,
                                                   valid_article)
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import valid_user


class CreateArticleSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(**valid_user)
        valid_article.update(
            {"author_id": self.user.id}
        )
        self.data = valid_article
        self.serializer_class = CreateArticleSerializer
        self.serializer = self.serializer_class(data=self.data)

    def test_serializer_can_validate_an_article(self):
        is_valid_article = self.serializer.is_valid(self.data)

        self.assertTrue(is_valid_article)

    def test_serializer_can_create_an_article(self):
        self.serializer.is_valid(self.data)
        article = self.serializer.save()

        self.assertIsInstance(article, Article)

    def test_serializer_raises_an_exception_on_request_without_a_title(self):
        article_without_title.update(
            {"author_id": self.user.id}
        )

        serializer = self.serializer_class(data=article_without_title)

        self.assertRaises(
            serializers.ValidationError,
            serializer.is_valid,
            raise_exception=True)
        self.assertRaisesMessage(
            serializers.ValidationError,
            'This field is required.',
            serializer.is_valid,
            article_without_title)

    def test_serializer_raises_an_exception_on_request_without_a_description(
            self):
        article_without_description.update(
            {"author_id": self.user.id}
        )

        serializer = self.serializer_class(data=article_without_description)

        self.assertRaises(
            serializers.ValidationError,
            serializer.is_valid,
            raise_exception=True)
        self.assertRaisesMessage(
            serializers.ValidationError,
            'This field is required.',
            serializer.is_valid,
            article_without_description)

    def test_serializer_raises_an_exception_on_request_without_a_body(self):
        article_without_body.update(
            {"author_id": self.user.id}
        )

        serializer = self.serializer_class(data=article_without_body)

        self.assertRaises(
            serializers.ValidationError,
            serializer.is_valid,
            raise_exception=True)
        self.assertRaisesMessage(
            serializers.ValidationError,
            'This field is required.',
            serializer.is_valid,
            article_without_body)

    def test_serializer_raises_an_exception_when_missing_author_id(self):
        valid_article.pop("author_id")
        article_without_author_id = valid_article

        serializer = self.serializer_class(data=article_without_author_id)

        self.assertRaises(
            serializers.ValidationError,
            serializer.is_valid,
            raise_exception=True)
        self.assertRaisesMessage(
            serializers.ValidationError,
            'This field is required.',
            serializer.is_valid,
            article_without_author_id)
