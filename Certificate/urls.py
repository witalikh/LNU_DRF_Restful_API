from django.urls import path
from .views import FirstCertificateAPIView, SecondCertificateAPIView

urlpatterns = [
    path('container/', FirstCertificateAPIView.as_view()),
    path('container/<identifier>', SecondCertificateAPIView.as_view())
]
