import re
from pprint import pprint

from rest_framework.authentication import BaseAuthentication

from base import services


class TokenAuthentication(BaseAuthentication):

    """
    Self-contained stateles authentication implementatrion
    that work similar to oauth2.
    It uses json web tokens (https://github.com/jpadilla/pyjwt) for trust
    data stored in the token.
    """

    auth_rx = re.compile(r"^Token (.+)$")

    def authenticate(self, request):
        # print(self.auth_rx)
        # pprint(request.META)
        if "HTTP_AUTHORIZATION" not in request.META:
            return None

        token_rx_match = self.auth_rx.search(
            request.META["HTTP_AUTHORIZATION"])
        if not token_rx_match:
            return None

        token = token_rx_match.group(1)
        # print(token)
        user = services.get_user_for_token(token, "authentication")
        # print(user)
        return (user, token)
