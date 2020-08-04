from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    # For OpenAPI we have to respect the Bearer format: `Authorization: Bearer <TOKEN>`
    keyword = 'Bearer'
