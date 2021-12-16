from django.utils.decorators import method_decorator
from rest_framework import status, filters

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from drf_yasg.utils import swagger_auto_schema

from .models import DoctorAppointment
from .serializers import DoctorAppointmentSerializer
from .docs import EndpointDocs
from algorithms.pagination import CustomOffsetPagination


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(**EndpointDocs.POST)
)
class DoctorAppointmentViewSet(ModelViewSet):
    """
    ViewSet for DoctorAppointment model
    Has .create, .delete, override .list and .retrieve
    """

    model = DoctorAppointment

    queryset = DoctorAppointment.objects.all()
    serializer_class = DoctorAppointmentSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    pagination_class = CustomOffsetPagination

    # all of these is allowed only for authenticated
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        """
        Create method envelope: user_id is defined from request
        """
        return serializer.save(user_id=self.request.user.pk)

    @swagger_auto_schema(**EndpointDocs.GET_LIST)
    def list(self, request, *args, **kwargs):
        """
        List method: get all meetings for current user
        """
        data = self.queryset.filter(user_id=request.user.pk)

        if len(data) == 0:
            return Response({"status": 404,
                             "message": "Requests for doctor meet not found"},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**EndpointDocs.GET)
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve method: find meeting with certain id for certain user
        """
        data = self.queryset.filter(user_id=request.user.pk,
                                    item_id=kwargs["identifier"])

        if len(data) == 0:
            return Response({"status": 404,
                             "message": "Requests for doctor meet not found"},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

