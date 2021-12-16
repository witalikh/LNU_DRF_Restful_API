from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, RefreshAPIView, LogoutAPIView

urlpatterns = [
   path('users/', RegistrationAPIView.as_view()),
   path('login/', LoginAPIView.as_view()),
   path('refresh/', RefreshAPIView.as_view()),
   path('logout/', LogoutAPIView.as_view())
]
