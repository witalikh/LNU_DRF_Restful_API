from django.utils.decorators import method_decorator
from rest_framework import status, filters

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import CertificateSerializer
from algorithms.permissions import IsAdminOrReadOnly
from algorithms.pagination import CustomOffsetPagination
from .models import Certificate
from .docs import EndpointDocs

from drf_yasg.utils import swagger_auto_schema



@method_decorator(
    name="get",
    decorator=swagger_auto_schema(**EndpointDocs.GET_LIST)
)
class FirstCertificateAPIView(ListAPIView):
    """
    (List)APIView class for "GET" and "POST" methods
    from url /api/container/
    "GET" is auto-defined (with filters and ordering) for getting certificates
    """

    # queryset and serializer for "GET" auto-define
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

    http_method_names = ["get", "post"]

    # custom filters
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["date_of_birth", "end_date", "id",
                     "international_passport", "start_date", "username", "vaccine"]

    # pagination
    pagination_class = CustomOffsetPagination

    # permissions
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(**EndpointDocs.POST)
    def post(self, request):
        """
        "POST" HTTP-request, append database with new certificate
        """
        serializer = CertificateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200,
                             "message": "Certificate successfully created",
                             "certificate": serializer.data},
                            status=status.HTTP_200_OK)

        else:
            return Response({"status": 400,
                            "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class SecondCertificateAPIView(APIView):
    """
    APIView class for "PUT", "GET" and "DELETE" requests
    from url /api/container/<some id to perform action with>
    """

    permission_classes = [IsAdminOrReadOnly]

    @staticmethod
    def get_object(identifier):
        """
        Helper method, looking for certificate with some id
        """
        try:
            return Certificate.objects.get(id=identifier)
        except Certificate.DoesNotExist:
            return None

    @swagger_auto_schema(**EndpointDocs.GET)
    def get(self, request, identifier):
        """
        "GET" HTTP-request, obtain certificate by id
        """
        certificate = self.get_object(identifier)
        if certificate is None:
            return Response({"status": 404,
                             "message": "Certificate not found"},
                            status=status.HTTP_404_NOT_FOUND)

        else:
            serializer = CertificateSerializer(certificate)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**EndpointDocs.PUT)
    def put(self, request, identifier):
        """
        "PUT" HTTP-request, edit the existing record (by id)
        """
        certificate = self.get_object(identifier)
        if certificate is None:
            return Response({"status": 404,
                             "message": "Certificate not found"},
                            status=status.HTTP_404_NOT_FOUND)

        certificate_data = JSONParser().parse(request)
        serializer = CertificateSerializer(certificate, data=certificate_data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200,
                             "message": "Certificate successfully updated",
                             "certificate": serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"status": 400,
                             "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**EndpointDocs.DELETE)
    def delete(self, request, identifier):
        """
        "DELETE" HTTP-request, delete certificate by id
        """
        certificate = self.get_object(identifier)
        if certificate is None:
            return Response({"status": 404,
                             "message": "Certificate not found"},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            certificate.delete()
            return Response({"status": 200,
                             "message": "Successfully deleted!"},
                            status=status.HTTP_200_OK)
