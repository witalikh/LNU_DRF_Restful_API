"""
Certificate app Swagger doc
"""
from .models import ModelConsts
from drf_yasg import openapi


class SwaggerDocDicts:

    CERTIFICATE_EXAMPLE = {
        "username": "string",
        "international_passport": "string",
        "date_of_birth": "yyyy-mm-dd",
        "start_date": "yyyy-mm-dd",
        "end_date": "yyyy-mm-dd",
        "vaccine": "Pfizer"
    }

    DENIED_ACCESS = {
      "detail": "Authentication credentials were not provided OR "
                "You do not have permission to perform this action."
    }

    CERTIFICATE_NOT_FOUND_RESPONSE = {
        "status": 404,
        "message": "Certificate not found"
    }

    CERTIFICATE_BAD = {
        "status": 400,
        "errors": {
            "field_1": "error_1",
            "field_2": "error_2"
        }
    }

    CERTIFICATE_CREATE_RESPONSE = {
        "status": 200,
        "message": "Certificate successfully created",
        "certificate": CERTIFICATE_EXAMPLE
    }

    CERTIFICATE_UPDATE_RESPONSE = {
        "status": 200,
        "message": "Certificate successfully updated",
        "certificate": CERTIFICATE_EXAMPLE
    }

    CERTIFICATE_DELETE_RESPONSE = {
        "status": 200,
        "message": "Successfully deleted!"
    }

    CERTIFICATE_INPUT_PARAMETER = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING,
                                       description='Full name',
                                       max_length=256),
            "international_passport": openapi.Schema(type=openapi.TYPE_STRING,
                                                     description='Passport code',
                                                     max_length=8),
            "date_of_birth": openapi.Schema(type=openapi.TYPE_STRING,
                                            description='Birthday Date',
                                            format="date"),
            "start_date": openapi.Schema(type=openapi.TYPE_STRING,
                                         description='Date of issue',
                                         format="date"),
            "end_date": openapi.Schema(type=openapi.TYPE_STRING,
                                       description='Date of expire',
                                       format="date"),
            "vaccine": openapi.Schema(type=openapi.TYPE_STRING,
                                      description="Vaccine",
                                      enum=ModelConsts.AVAILABLE_VACCINES,
                                      max_length=64),
        })


class EndpointDocs:
    GET_LIST = {
        "operation_description": "Get list of all CovidCertificates from database",
        "responses": {
            "200": openapi.Response(
                description="Valid id -> obtain list of all certificates from database",
                examples={
                    "application/json": [
                        SwaggerDocDicts.CERTIFICATE_EXAMPLE,
                    ]
                }
            ),
        }
    }

    POST = {
        "request_body": SwaggerDocDicts.CERTIFICATE_INPUT_PARAMETER,
        "operation_description": "Insert new CovidCertificate into a database",
        "responses": {
            "200": openapi.Response(
                description="Valid certificate sent -> write to database",
                examples={
                    "application/json": SwaggerDocDicts.CERTIFICATE_CREATE_RESPONSE
                }
            ),
            "400": openapi.Response(
                description="Invalid certificate sent -> discard",
                examples={
                    "application/json": SwaggerDocDicts.CERTIFICATE_BAD
                }
            ),
            "403": openapi.Response(
                description="Not authenticated / not admin -> access denied",
                examples={
                    "application/json": SwaggerDocDicts.DENIED_ACCESS
                }
            ),
        }
    }

    GET = {
        "operation_description": "Get CovidCertificate by id from database",
        "responses": {
            "200": openapi.Response(
                description="Valid id -> obtain certificate from database",
                examples={
                    "application/json": SwaggerDocDicts.CERTIFICATE_EXAMPLE
                }
            ),
            "404": openapi.Response(
                description="Invalid id -> response HTTP 404",
                examples={
                    "application/json": SwaggerDocDicts.CERTIFICATE_NOT_FOUND_RESPONSE
                }
            ),
        }
    }

    PUT = {
        "request_body": SwaggerDocDicts.CERTIFICATE_INPUT_PARAMETER,
        "operation_description": "Edit CovidCertificate record by ID in database",
        "responses": {
            "200": openapi.Response(
                description="Valid id -> obtain certificate from database",
                examples={
                    "application/json": SwaggerDocDicts.CERTIFICATE_UPDATE_RESPONSE
                }
            ),
            "400": openapi.Response(
                description="Invalid certificate sent -> discard",
                examples={
                    "application/json": SwaggerDocDicts.CERTIFICATE_BAD
                }
            ),
            "404": openapi.Response(
                description="Invalid id -> response HTTP 404",
                examples={
                    "application/json": SwaggerDocDicts.CERTIFICATE_NOT_FOUND_RESPONSE
                }
            ),
            "403": openapi.Response(
                description="Not authenticated / not admin -> access denied",
                examples={
                    "application/json": SwaggerDocDicts.DENIED_ACCESS
                }
            ),
        }
    }

    DELETE = {
        "operation_description": "Delete CovidCertificate by id from database",
        "responses": {
            "200": openapi.Response(
                description="Valid id -> obtain certificate from database",
                examples={
                    "application/json": SwaggerDocDicts.CERTIFICATE_DELETE_RESPONSE
                }
            ),
            "404": openapi.Response(
                description="Invalid id -> response HTTP 404",
                examples={
                    "application/json": SwaggerDocDicts.CERTIFICATE_NOT_FOUND_RESPONSE
                }
            ),
            "403": openapi.Response(
                description="Not authenticated / not admin -> access denied",
                examples={
                    "application/json": SwaggerDocDicts.DENIED_ACCESS
                }
            ),
        }
    }
