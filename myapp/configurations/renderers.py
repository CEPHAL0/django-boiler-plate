# renderers.py
from rest_framework.renderers import JSONRenderer
from rest_framework import status as h

class ApiWrapperRenderer(JSONRenderer):
    """
    Wraps all responses (including errors) with:
    {
        "status": "Success|Error",
        "status_code": 200,
        "message": "OK",
        "data": { ... }
    }
    """

    # Map status codes to default messages
    DEFAULT_MESSAGES = {
        h.HTTP_200_OK: "Operation Successful",
        h.HTTP_400_BAD_REQUEST: "Bad Request",
        h.HTTP_401_UNAUTHORIZED: "Authentication credentials were not provided.",
        h.HTTP_403_FORBIDDEN: "You do not have permission to perform this action.",
        h.HTTP_404_NOT_FOUND: "The requested resource was not found.",
        h.HTTP_405_METHOD_NOT_ALLOWED: "Method not allowed.",
        h.HTTP_500_INTERNAL_SERVER_ERROR: "An internal server error occurred.",
    }

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not renderer_context:
            return super().render(data, accepted_media_type, renderer_context)

        response = renderer_context['response']
        status_code = response.status_code
        current_data = data or {}

        message = self.DEFAULT_MESSAGES.get(status_code, "An error occurred")

        if isinstance(current_data, dict):
            if "detail" in current_data:
                message = current_data.pop("detail")
            elif "message" in current_data:
                message = current_data.pop("message")

            data = current_data.pop("data", current_data)

        status = "Error" if status_code >= 400 else "Success"

        wrapped_data = {
            "status": status,
            "status_code": status_code,
            "message": message,
            "data": data,
        }

        response.data = wrapped_data

        return super().render(wrapped_data, accepted_media_type, renderer_context)
