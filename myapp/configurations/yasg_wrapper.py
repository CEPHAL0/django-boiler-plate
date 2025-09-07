from rest_framework import serializers
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ResponseWrapperSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["Success", "Error"])
    status_code = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.JSONField()


def make_response_serializer(
    data_serializer_or_example,
    ref_name: str,
    status_example="Success",
    status_code_example=200,
    message_example="Operation successful",
):
    """
    Create a wrapper serializer for responses.
    - data_serializer_or_example can be:
        * Serializer class
        * dict of field_name -> Serializer class
        * dict (example only, no schema introspection)
        * callable returning serializer
    """

    # Case 1: dict of serializers
    if isinstance(data_serializer_or_example, dict) and all(
        isinstance(v, type) and issubclass(v, serializers.BaseSerializer)
        for v in data_serializer_or_example.values()
    ):
        fields = {key: ser() for key, ser in data_serializer_or_example.items()}
        Nested = type(
            f"{ref_name}Nested",
            (serializers.Serializer,),
            {**fields, "Meta": type("Meta", (), {"ref_name": f"{ref_name}Nested"})},
        )
        data_field = Nested()

    # Case 2: serializer class
    elif isinstance(data_serializer_or_example, type) and issubclass(
        data_serializer_or_example, serializers.BaseSerializer
    ):
        data_field = data_serializer_or_example()

    # Case 3: callable returning serializer
    elif callable(data_serializer_or_example):
        data_field = data_serializer_or_example()

    # Case 4: dict (raw example, not schema)
    elif isinstance(data_serializer_or_example, dict):
        # Represent as JSONField in schema, but example will show real structure
        data_field = serializers.JSONField()

    # Case 5: nothing provided
    else:
        data_field = serializers.Serializer()

    attrs = {
        "status": serializers.ChoiceField(
            choices=["Success", "Error"], default=status_example
        ),
        "status_code": serializers.IntegerField(default=status_code_example),
        "message": serializers.CharField(default=message_example),
        "data": data_field,
        "Meta": type("Meta", (), {"ref_name": ref_name}),
    }
    return type(f"{ref_name}Wrapper", (serializers.Serializer,), attrs)



def swagger_response(
    *,
    output_serializer=None,
    input_serializer=None,
    many: bool = False,
    responses: dict = None,
    include_forbidden: bool = True,
):
    """
    Flexible decorator for swagger_auto_schema:
    - output_serializer: the default serializer used inside `data` for 200 responses
    - input_serializer: request body serializer (optional, only for POST/PUT/PATCH/DELETE)
    - many: if True, `data` will be a list
    - responses: dict of status_code -> {"serializer": Serializer|dict, "desc": str, "message": str}
    - include_forbidden: whether to always include a 403 response
    """
    def decorator(func):
        ref_base = func.__qualname__
        final_responses = {}

        if responses:
            for code, opts in responses.items():
                serializer_cls = opts.get("serializer", serializers.Serializer)
                desc = opts.get("desc", "Response")
                # 👇 auto-pick message unless explicitly set
                msg = opts.get("message") or (
                    "Success" if code < 400 else "Error"
                )

                wrapped = make_response_serializer(
                    serializer_cls,
                    ref_name=f"{ref_base}{code}Response",
                    status_example="Error" if code >= 400 else "Success",
                    status_code_example=code,
                    message_example=msg,   # <-- used only as example
                )
                final_responses[code] = openapi.Response(description=desc, schema=wrapped)

        if output_serializer and 200 not in final_responses:
            wrapped = make_response_serializer(
                output_serializer,
                ref_name=f"{ref_base}200Response",
                status_example="Success",
                status_code_example=200,
                message_example="Success",   # auto-default
            )
            final_responses[200] = openapi.Response(description="Successful response", schema=wrapped)

        if include_forbidden and 403 not in final_responses:
            wrapped = make_response_serializer(
                serializers.Serializer,
                ref_name=f"{ref_base}403Response",
                status_example="Error",
                status_code_example=403,
                message_example="Forbidden",
            )
            final_responses[403] = openapi.Response(description="Forbidden", schema=wrapped)

        # request_body only for methods that support it
        body = None
        if input_serializer and func.__name__.lower() in ["post", "put", "patch", "delete"]:
            body = input_serializer

        return swagger_auto_schema(
            request_body=body,
            responses=final_responses,
        )(func)

    return decorator
