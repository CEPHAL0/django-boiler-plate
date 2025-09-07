# schemas.py
from drf_yasg import openapi

def wrapped_response(serializer=None, example_message="Operation successful", is_list=False):
    # If serializer is provided, use it in a way drf-yasg recognizes
    if serializer:
        inner_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            title=serializer.__name__  # Helps Swagger register it
        )
        if is_list:
            data_schema = openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=inner_schema
            )
        else:
            data_schema = inner_schema
    else:
        data_schema = openapi.Schema(type=openapi.TYPE_OBJECT)

    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING),
            'status_code': openapi.Schema(type=openapi.TYPE_INTEGER),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'data': data_schema,
        },
        example={
            'status': 'Success',
            'status_code': 200,
            'message': example_message,
            'data': [] if is_list else {}
        }
    )