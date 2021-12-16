from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt


def decode_jwt_token(token, secret=settings.SECRET_KEY):
    """
    Helper function for decoding jwt token
    """

    # decode token
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256", ])

    except jwt.exceptions.ExpiredSignatureError:
        raise AuthenticationFailed(
            "The given token already expired."
        )

    # find user
    try:
        user = User.objects.get(id=payload['id'])

    except User.DoesNotExist:
        raise AuthenticationFailed(
            "Cannot identify any user by this token."
        )

    return {
        "user": user,
        "token_type": payload["token_type"]
    }
