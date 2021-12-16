"""
DoctorAppointment Swagger Docs
"""
from drf_yasg import openapi


class SwaggerDocDicts:
    DENIED_ACCESS = {
      "detail": "Authentication credentials were not provided."
    }

    ORDER_NOT_FOUND = {
      "status": 404,
      "message": "Requests for doctor meet not found"
    }

    SAMPLE_GET_ORDER = {
        "item_id": 0,
        "user_id": 0,
        "doctor_fullname": "John Doe",
        "start_datetime": "yyyy-mm-ddThh:mm:ss.millisZ",
        "end_datetime": "yyyy-mm-ddThh:mm:ss.millisZ"
    }

    SAMPLE_INVALID_POST = {
      "field_1": [
        "error_1", "error_2"
      ],
      "field_2": [
        "error_1", "error_2"
      ]
    }


class EndpointDocs:
    GET_LIST = {
        "operation_description": "Get all orders of current user",
        "responses": {
            "200": openapi.Response(
                description="Show all orders if found",
                examples={
                    "application/json": [SwaggerDocDicts.SAMPLE_GET_ORDER] * 2
                }
            ),
            "403": openapi.Response(
                description="Not authenticated / not admin -> access denied",
                examples={
                    "application/json": SwaggerDocDicts.DENIED_ACCESS
                }
            ),
            "404": openapi.Response(
                description="No such id => 404",
                examples={
                    "application/json": SwaggerDocDicts.ORDER_NOT_FOUND
                }
            ),
        }
    }

    GET = {
        "operation_description": "Get order by identifier",
        "responses": {
            "200": openapi.Response(
                description="Show one order if found",
                examples={
                    "application/json": SwaggerDocDicts.SAMPLE_GET_ORDER
                }
            ),
            "403": openapi.Response(
                description="Not authenticated / not admin -> access denied",
                examples={
                    "application/json": SwaggerDocDicts.DENIED_ACCESS
                }
            ),
            "404": openapi.Response(
                description="No such id => 404",
                examples={
                    "application/json": SwaggerDocDicts.ORDER_NOT_FOUND
                }
            ),
        }
    }

    POST = {
        "operation_description": "Post order with body",
        "responses": {
            "200": openapi.Response(
                description="Valid order sent -> write to database",
                examples={
                    "application/json": SwaggerDocDicts.SAMPLE_GET_ORDER
                }
            ),
            "403": openapi.Response(
                description="Not authenticated / not admin -> access denied",
                examples={
                    "application/json": SwaggerDocDicts.DENIED_ACCESS
                }
            ),
            "400": openapi.Response(
                description="Bad input => 400",
                examples={
                    "application/json": SwaggerDocDicts.SAMPLE_INVALID_POST
                }
            ),
        }
    }
