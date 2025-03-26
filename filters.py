from flask import request, Flask

from res import BizException, Codes, R


def register_filters(app: Flask, app_configurations: dict):
    """
    Register Filters.
    """

    @app.before_request
    def token_filter():
        white_apis = app_configurations['server']['white_apis']
        if request.path not in white_apis:
            token = request.headers.get('Authorization')
            expected = app_configurations['server']['token']
            if token != expected:
                e = BizException.from_codes(Codes.UNAUTHORIZED)
                return R.error(e).json_response()
