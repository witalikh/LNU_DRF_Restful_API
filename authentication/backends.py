from rest_framework import authentication, exceptions
from .decode import decode_jwt_token
from .models import BlacklistedToken


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom backend for authentication with JWT Tokens
    """

    # prefix before every Token
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        """
        Method for endpoints to authenticate with jwt-tokens
        """
        request.user = None

        # decompose header content
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        # nothing in header
        if not auth_header:
            return None

        # not enough args
        if len(auth_header) == 1:
            return None

        # a lot of args
        elif len(auth_header) > 2:
            return None

        else:
            # split decomposed header content into vars
            prefix = auth_header[0].decode('utf-8')
            token = auth_header[1].decode('utf-8')

            # check prefix
            if prefix.lower() != auth_header_prefix.lower():
                return None

            else:
                return self._validate_token(request, token)

    @staticmethod
    def _validate_token(request, token):
        """
        Private method for checking token's validity
        """
        decoded = decode_jwt_token(token)

        # reject any non-access tokens
        if decoded["token_type"] != "access":
            raise exceptions.AuthenticationFailed(
                "Authentication cannot be performed on non-access tokens"
            )

        if BlacklistedToken.objects.filter(token=token).count():
            raise exceptions.AuthenticationFailed(
                "Token is blacklisted for logout"
            )

        return decoded["user"], token
