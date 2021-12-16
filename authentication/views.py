from rest_framework import status, exceptions

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from .serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer
from .decode import decode_jwt_token
from .docs import EndpointDocs


class RegistrationAPIView(APIView):
    """
    APIView for registration a new user
    Any user can register, but only ordinary user
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(**EndpointDocs.REGISTER)
    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """
    APIView for login
    Any user can login, including admins
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(**EndpointDocs.LOGIN)
    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RefreshAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    @staticmethod
    @swagger_auto_schema(**EndpointDocs.REFRESH)
    def post(request):
        """
        Validate refresh token that is in json body
        """

        data = request.data
        decoded = decode_jwt_token(data["refresh_token"])

        if decoded["token_type"] != "refresh":
            raise exceptions.AuthenticationFailed(
                "This is not a refresh token")

        else:
            user = decoded["user"]
            if user == request.user:
                return Response({
                        "token": user.token,
                        "refresh_token": user.refresh_token
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response({
                    "Error": "Access denied"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    @swagger_auto_schema(**EndpointDocs.LOGOUT)
    def post(self, request):
        auth_value = request.headers.get("Authorization")
        token = auth_value.split()[1]

        serializer = self.serializer_class(data={
            "token": token
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Token blacklisted successfully"},
            status=status.HTTP_200_OK)
