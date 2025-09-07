from django.conf import settings
from rest_framework.views import exception_handler
from rest_framework import status
from myapp.utils.env_constants import env
from myapp.configurations.logging import logger
from myapp.utils.responses import error


def global_exception_handler(exc, context):
    response = exception_handler(exc, context)

    request = context.get("request")
    view = context.get("view")

    logger.error(
        "Unhandled exception in %s: %s (Path: %s, Method: %s)",
        view.__class__.__name__ if view else "UnknownView",
        str(exc),
        request.path if request else "UnknownPath",
        request.method if request else "UnknownMethod",
        exc_info=True,
    )

    if response is not None:
        return response

    environment = env.environment
    if environment == "development":
        detail = str(exc)
    else:
        detail = "Server Error"

    return error(
        message="Internal Server error occurred",
        details=detail,
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
