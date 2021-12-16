from django.urls import path
from .views import DoctorAppointmentViewSet

urlpatterns = [
    path('', DoctorAppointmentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<identifier>', DoctorAppointmentViewSet.as_view({'get': 'retrieve'}))
]
