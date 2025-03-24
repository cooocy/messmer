from flask import Flask, request, jsonify

from core.configurations import ConfigurationRepository
from responses.exceptions import BizException, Codes
from responses.results import R


class ConfigFileController:
    def __init__(self,
                 app: Flask,
                 app_configurations__: dict,
                 repository: ConfigurationRepository):
        self.app = app
        self.app_configurations__ = app_configurations__
        self.repository = repository
        self.register_routes()

    def register_routes(self):
        """
        Register routes.
        """

        @self.app.route('/cf/save', methods=['POST'])
        def save():
            request_body: dict = request.json
            print(f'Request Body: {request_body}')
            namespace = request_body.get('namespace', '')
            name = request_body.get('name', '')
            content = request_body.get('content', '')
            if namespace == '' or name == '' or content == '':
                raise BizException.from_codes(Codes.ARGS_ERROR)

            configuration = self.repository.save(namespace, name, content)
            r = R.ok(configuration)
            return jsonify(r)

        @self.app.route('/cf/read', methods=['GET'])
        def read():
            namespace = request.args.get('namespace', '')
            name = request.args.get('name', '')
            if namespace == '' or name == '':
                raise BizException.from_codes(Codes.ARGS_ERROR)

            configuration = self.repository.get(namespace, name)
            r = R.ok(configuration)
            return jsonify(r)
