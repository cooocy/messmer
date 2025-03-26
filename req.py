import json

from flask import request


def get_json_body() -> dict:
    """
    Get Json Request Body.
    """

    request_body = request.json
    if type(request_body) is str:
        request_body = json.loads(request_body)
    return request_body
