from rest_framework import serializers

from authors.apps.authentication.models import User
from authors.apps.authentication.serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist

from .models import Article


class CreateArticleSerializer(serializers.ModelSerializer):
    """Serializes create article requests and creates an article"""

    title = serializers.CharField(max_length=255, min_length=2)
    description = serializers.CharField()
    body = serializers.CharField()
    author_id = serializers.IntegerField()

    class Meta:
        model = Article

        fields = ['title', 'description', 'body', 'author_id']

    def validate(self, data):
        author_id = data.pop('author_id', None)
        author = User.objects.get(id=author_id)
        data.update({'author': author})

        return data

    def create(self, validated_data):
        return Article.objects.create(**validated_data)
