from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import ArticleJSONRenderer
from .serializers import CreateArticleSerializer


class CreateArticleAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = CreateArticleSerializer

    def post(self, request):
        article = request.data.get('article', {})
        article.update({"author_id": request.user.id})

        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        saved_article = serializer.save()
        serializer.validated_data.update({"article": saved_article})

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED)
