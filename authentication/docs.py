"""
Authentication app Swagger docs
"""
from drf_yasg import openapi


class SwaggerDocDicts:
    LOGIN_SUCCESS = {
        "email": "john.doe@example.com",
        "token": "JWT-token "
    }

    LOGIN_FAIL = {
        "field_1 OR non_field_errors": [
            "error_1", "error_2"
        ],
        "field_2": [
            "error_1", "error_2"
        ],
    }

    LOGOUT_SUCCESS = {
        "message": "Token blacklisted successfully"
    }

    REGISTER_SUCCESS = {
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "token": "JWT-token"
    }

    REGISTER_FAIL = {
        "field_1": [
            "error_1", "error_2"
        ],
        "field_2": [
            "error_1", "error_2"
        ]
    }

    REFRESH_SUCCESS = {
        "token": "valid access token",
        "refresh_token": "valid refresh token"
    }

    REFRESH_FAIL = {
        "detail": "reason of fail"
    }

    REGISTER_PARAMETER = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING,
                                    description='email',
                                    max_length=254),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING,
                                         description='First name',
                                         max_length=128),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING,
                                        description='Last Name',
                                        max_length=128),
            "password": openapi.Schema(type=openapi.TYPE_STRING,
                                       description='Password',
                                       max_length=128),
        })

    LOGIN_PARAMETER = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING,
                                    description='email',
                                    max_length=254),
            "password": openapi.Schema(type=openapi.TYPE_STRING,
                                       description='Password',
                                       max_length=128),
        })

    REFRESH_PARAMETER = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "refresh_token": openapi.Schema(type=openapi.TYPE_STRING,
                                            description='valid refresh token',
                                            max_length=255),
        })


class EndpointDocs:

    LOGIN = {
        "request_body": SwaggerDocDicts.LOGIN_PARAMETER,
        "operation_description": "Login and generate jwt token",
        "responses": {
            "200": openapi.Response(
                description="Valid data => login (generate JWT)",
                examples={
                    "application/json": SwaggerDocDicts.LOGIN_SUCCESS
                }
            ),
            "400": openapi.Response(
                description="Invalid data => no login",
                examples={
                    "application/json": SwaggerDocDicts.LOGIN_FAIL
                }
            ),
        }
    }

    LOGOUT = {
        "operation_description": "Logout: blacklist jwt token",
        "responses": {
            "200": openapi.Response(
                description="Valid token in header => logout (blacklist JWT)",
                examples={
                    "application/json": SwaggerDocDicts.LOGOUT_SUCCESS
                }
            ),
            "400": openapi.Response(
                description="Invalid data => no logout perform",
                examples={
                    "application/json": SwaggerDocDicts.LOGIN_FAIL
                }
            ),
        }
    }

    REGISTER = {
        "request_body": SwaggerDocDicts.REGISTER_PARAMETER,
        "operation_description": "Register new user and login (obtain new jwt token)",
        "responses": {
            "201": openapi.Response(
                description="Valid data, unique email => register + JWT",
                examples={
                    "application/json": SwaggerDocDicts.REGISTER_SUCCESS
                }
            ),
            "400": openapi.Response(
                description="Invalid input parameters = no registration",
                examples={
                    "application/json": SwaggerDocDicts.REGISTER_FAIL
                }
            ),
        }
    }

    REFRESH = {
        "request_body": SwaggerDocDicts.REFRESH_PARAMETER,
        "operation_description": "Refresh token by given refresh token",
        "responses": {
            "201": openapi.Response(
                description="Valid data, unique email => register + JWT",
                examples={
                    "application/json": SwaggerDocDicts.REFRESH_SUCCESS
                }
            ),
            "403": openapi.Response(
                description="Invalid input parameters = no registration",
                examples={
                    "application/json": SwaggerDocDicts.REFRESH_FAIL
                }
            ),
        }
    }
