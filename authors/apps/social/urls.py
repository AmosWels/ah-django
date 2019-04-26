from django.urls import path

from .views import FacebookAuthAPIView, GoogleAuthAPIView, TwitterAuthAPIView

app_name = "social-auth"
urlpatterns = [
    path('social-auth/facebook/', FacebookAuthAPIView.as_view(), name='facebook-auth'),
    path('social-auth/google/', GoogleAuthAPIView.as_view(), name='google-auth'),
    path('social-auth/twitter/', TwitterAuthAPIView.as_view(), name='twiiter-auth')
]
