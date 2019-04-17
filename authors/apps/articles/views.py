from django.http import Http404
from django.core import exceptions

from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from .models import Article
from .renderers import ArticleJSONRenderer
from .permissions import IsOwnerOrReadOnly
from .serializers import ArticleSerializer
from .exceptions import ArticleDoesNotExist


class ListCreateArticleAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def post(self, request):
        article = request.data.get('article', {})
        user_data = {"author": request.user.profile}
        serializer = self.serializer_class(data=article, context=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        articles = Article.objects.filter().order_by('-created_at')
        serializer = self.serializer_class(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveArticleApiView(RetrieveUpdateDestroyAPIView):
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    permission_classes = (IsOwnerOrReadOnly,IsAuthenticatedOrReadOnly)
    lookup_field = 'slug'
    queryset = Article.objects.select_related('author')
    def update(self, request, slug, *args, **kwargs):
        try:
            article_to_update = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise ArticleDoesNotExist

        if request.user != article_to_update.author.user:
            raise exceptions.PermissionDenied()
            
        new_article = request.data.get("article", {})
        serializer = self.serializer_class(
            article_to_update, data=new_article, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug):
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        serializer = self.serializer_class(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, slug, *args, **kwargs):
        try:
            article = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise ArticleDoesNotExist
        
        self.check_object_permissions(self.request, article)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
