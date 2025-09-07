# responses.py
from typing import Union

from rest_framework.response import Response

def success(message: str, payload=None, status=200):
    """
    Return a success response.
    - payload: the actual data (e.g., serializer.data)
    - message: human-readable message
    - status: HTTP status code
    """

    if payload is not None:
        # If payload is a dict, merge its fields into body
        if isinstance(payload, dict):
            payload["message"] = message
        elif isinstance(payload, list):
            payload = {"message": message, "data":payload}
    else:
        payload = {"message": message, "data": {}}

    return Response(payload, status=status)

def error(message: str="An error occurred", details:Union[dict,list,str]=None, status:int=400):
    """
    Return error response.
    - message: string
    - details: any JSON-serializable data to go into the wrapper's "data" field
    """
    body = {'message': message}

    body['data'] = details or {}


    return Response(body, status=status)

# Optional: Shortcuts
def created(data=None, message="Resource created"):
    return success(data, message, status=201)

def no_content():
    return Response(status=204)