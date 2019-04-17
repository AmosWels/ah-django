from django.conf.urls import url
from django.urls import path

from .views import (
    ListCreateArticleAPIView, RetrieveArticleApiView
)

urlpatterns = [
    path('articles/', ListCreateArticleAPIView.as_view()),
    path('articles/<slug:slug>/', RetrieveArticleApiView.as_view())
]

